package org.embasic.pdfeditor.workspace

/** Clean-room, platform-neutral proof of concept. No PDF bytes, URI, path or renderer handles. */
data class SourceDocumentRef(val id: String, val pageCount: Int) {
    init {
        require(id.isNotBlank()) { "source ID must not be blank" }
        require(pageCount in 1..10_000) { "unsupported source page count" }
    }
}

data class EditorPageRef(
    val id: String,
    val sourceId: String,
    val sourcePageIndex: Int,
    val quarterTurns: Int = 0,
) {
    init {
        require(id.isNotBlank() && sourceId.isNotBlank()) { "page/source ID must not be blank" }
        require(sourcePageIndex >= 0) { "negative source page index" }
        require(quarterTurns in 0..3) { "rotation must be normalized" }
    }
}

/** Copies on ingress and egress; callers cannot mutate the underlying selection. */
class SelectionState private constructor(private val storedIds: Set<String>) {
    val pageIds: Set<String> get() = storedIds.toSet()

    companion object {
        fun empty(): SelectionState = SelectionState(emptySet())
        fun of(ids: Collection<String>): SelectionState = SelectionState(ids.toSet())
    }
}

/** Snapshot invariant: stable unique IDs, valid page origins, and in-document selection. */
class EditorDocumentState private constructor(
    private val storedSources: List<SourceDocumentRef>,
    private val storedPages: List<EditorPageRef>,
    val selection: SelectionState,
) {
    val sources: List<SourceDocumentRef> get() = storedSources.toList()
    val pages: List<EditorPageRef> get() = storedPages.toList()

    init {
        require(storedSources.map { it.id }.toSet().size == storedSources.size) { "duplicate source ID" }
        require(storedPages.map { it.id }.toSet().size == storedPages.size) { "duplicate page ID" }
        val sourceById = storedSources.associateBy { it.id }
        for (page in storedPages) {
            val source = sourceById[page.sourceId] ?: throw IllegalArgumentException("unknown page source")
            require(page.sourcePageIndex < source.pageCount) { "page index outside source" }
        }
        require(selection.pageIds.all { id -> storedPages.any { it.id == id } }) { "selection contains missing page" }
    }

    internal fun with(
        sources: List<SourceDocumentRef> = storedSources,
        pages: List<EditorPageRef> = storedPages,
        selection: SelectionState = this.selection,
    ): EditorDocumentState = EditorDocumentState(sources.toList(), pages.toList(), selection)

    companion object {
        fun empty(): EditorDocumentState = EditorDocumentState(emptyList(), emptyList(), SelectionState.empty())
    }
}

sealed interface EditorAction {
    /** Import is model-only; a platform adapter must bind the opaque source ID to verified bytes. */
    data class ImportSource(val source: SourceDocumentRef, val pageIds: List<String>) : EditorAction
    data class MovePage(val pageId: String, val targetIndex: Int) : EditorAction
    data class RotatePage(val pageId: String, val clockwiseQuarterTurns: Int) : EditorAction
    data class DuplicatePage(val pageId: String, val newPageId: String) : EditorAction
    data class DeletePages(val pageIds: Set<String>) : EditorAction
    data class SelectPages(val pageIds: Set<String>) : EditorAction
}

object EditorReducer {
    fun reduce(state: EditorDocumentState, action: EditorAction): EditorDocumentState {
        val pages = state.pages
        return when (action) {
            is EditorAction.ImportSource -> {
                require(state.sources.none { it.id == action.source.id }) { "source already imported" }
                val ids = action.pageIds.toList()
                require(ids.size == action.source.pageCount && ids.toSet().size == ids.size) { "page ID count mismatch" }
                require(ids.all { it.isNotBlank() && pages.none { page -> page.id == it } }) { "page ID collision" }
                val imported = ids.mapIndexed { index, id -> EditorPageRef(id, action.source.id, index) }
                state.with(sources = state.sources + action.source, pages = pages + imported)
            }
            is EditorAction.MovePage -> {
                val from = pages.indexOfFirst { it.id == action.pageId }
                require(from >= 0 && action.targetIndex in pages.indices) { "invalid move" }
                if (from == action.targetIndex) state else {
                    val reordered = pages.toMutableList()
                    val page = reordered.removeAt(from)
                    reordered.add(action.targetIndex, page)
                    state.with(pages = reordered)
                }
            }
            is EditorAction.RotatePage -> {
                val index = pages.indexOfFirst { it.id == action.pageId }
                require(index >= 0) { "unknown page" }
                val turns = ((action.clockwiseQuarterTurns % 4) + 4) % 4
                if (turns == 0) state else {
                    val updated = pages.toMutableList()
                    updated[index] = pages[index].copy(quarterTurns = (pages[index].quarterTurns + turns) % 4)
                    state.with(pages = updated)
                }
            }
            is EditorAction.DuplicatePage -> {
                val index = pages.indexOfFirst { it.id == action.pageId }
                require(index >= 0 && action.newPageId.isNotBlank() && pages.none { it.id == action.newPageId }) { "invalid duplicate" }
                val updated = pages.toMutableList()
                updated.add(index + 1, pages[index].copy(id = action.newPageId))
                state.with(pages = updated)
            }
            is EditorAction.DeletePages -> {
                val ids = action.pageIds.toSet()
                require(ids.all { id -> pages.any { it.id == id } }) { "unknown deleted page" }
                if (ids.isEmpty()) state else state.with(
                    pages = pages.filterNot { it.id in ids },
                    selection = SelectionState.of(state.selection.pageIds - ids),
                )
            }
            is EditorAction.SelectPages -> {
                val ids = action.pageIds.toSet()
                require(ids.all { id -> pages.any { it.id == id } }) { "unknown selected page" }
                if (ids == state.selection.pageIds) state else state.with(selection = SelectionState.of(ids))
            }
        }
    }
}

/** Bounded, persistent undo/redo history. Selection-only changes do not create undo entries. */
class EditorHistory private constructor(
    val current: EditorDocumentState,
    private val undoSnapshots: List<EditorDocumentState>,
    private val redoSnapshots: List<EditorDocumentState>,
    val capacity: Int,
) {
    val undoDepth: Int get() = undoSnapshots.size
    val redoDepth: Int get() = redoSnapshots.size

    fun dispatch(action: EditorAction): EditorHistory {
        val next = EditorReducer.reduce(current, action)
        if (next === current) return this
        if (action is EditorAction.SelectPages) return EditorHistory(next, undoSnapshots, redoSnapshots, capacity)
        return EditorHistory(next, (undoSnapshots + current).takeLast(capacity), emptyList(), capacity)
    }

    // Selection is transient UI state: keep it across undo/redo for pages that still exist.
    private fun retainSelection(target: EditorDocumentState): EditorDocumentState {
        val validIds = target.pages.map { it.id }.toSet()
        return target.with(selection = SelectionState.of(current.selection.pageIds.intersect(validIds)))
    }

    fun undo(): EditorHistory = if (undoSnapshots.isEmpty()) this else EditorHistory(
        retainSelection(undoSnapshots.last()), undoSnapshots.dropLast(1), (redoSnapshots + current).takeLast(capacity), capacity,
    )

    fun redo(): EditorHistory = if (redoSnapshots.isEmpty()) this else EditorHistory(
        retainSelection(redoSnapshots.last()), (undoSnapshots + current).takeLast(capacity), redoSnapshots.dropLast(1), capacity,
    )

    companion object {
        fun start(capacity: Int = 32): EditorHistory {
            require(capacity in 1..128) { "history capacity must be bounded" }
            return EditorHistory(EditorDocumentState.empty(), emptyList(), emptyList(), capacity)
        }
    }
}

data class EditorExportPage(val sourceId: String, val sourcePageIndex: Int, val quarterTurns: Int)

/** Export is a declarative snapshot, not a PDF engine or filesystem operation. */
class EditorExportPlan private constructor(
    private val storedSources: List<SourceDocumentRef>,
    private val storedPages: List<EditorExportPage>,
) {
    val sources: List<SourceDocumentRef> get() = storedSources.toList()
    val pages: List<EditorExportPage> get() = storedPages.toList()

    companion object {
        fun from(state: EditorDocumentState): EditorExportPlan {
            require(state.pages.isNotEmpty()) { "cannot export empty document" }
            return EditorExportPlan(
                state.sources.toList(),
                state.pages.map { EditorExportPage(it.sourceId, it.sourcePageIndex, it.quarterTurns) },
            )
        }
    }
}
