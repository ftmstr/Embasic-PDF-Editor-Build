package org.embasic.pdfeditor.workspace

/** Isolated JVM smoke harness, not Gradle/KMP/platform acceptance. */
private var executed = 0
private fun scenario(name: String, block: () -> Unit) {
    block()
    executed++
    println("PASS: $name")
}
private inline fun <reified T : Throwable> rejects(noinline block: () -> Unit) {
    try { block() } catch (e: Throwable) { if (e is T) return else throw e }
    error("expected ${T::class.simpleName}")
}
private fun base() = EditorHistory.start().dispatch(
    EditorAction.ImportSource(SourceDocumentRef("s1", 3), listOf("p1", "p2", "p3"))
)
fun main() {
    scenario("empty workspace") { check(EditorHistory.start().current.pages.isEmpty()) }
    scenario("import source") { check(base().current.pages.map { it.id } == listOf("p1", "p2", "p3")) }
    scenario("reject duplicate page IDs") { rejects<IllegalArgumentException> { EditorHistory.start().dispatch(EditorAction.ImportSource(SourceDocumentRef("s1", 2), listOf("x", "x"))) } }
    scenario("reject import count mismatch") { rejects<IllegalArgumentException> { EditorHistory.start().dispatch(EditorAction.ImportSource(SourceDocumentRef("s1", 2), listOf("x"))) } }
    scenario("reject duplicate source") { rejects<IllegalArgumentException> { base().dispatch(EditorAction.ImportSource(SourceDocumentRef("s1", 1), listOf("x"))) } }
    scenario("move to end") { check(base().dispatch(EditorAction.MovePage("p1", 2)).current.pages.map { it.id } == listOf("p2", "p3", "p1")) }
    scenario("reject out-of-range move") { rejects<IllegalArgumentException> { base().dispatch(EditorAction.MovePage("p1", 3)) } }
    scenario("rotate wraps negative") { check(base().dispatch(EditorAction.RotatePage("p1", -1)).current.pages.first().quarterTurns == 3) }
    scenario("rotate large offset safely") { check(base().dispatch(EditorAction.RotatePage("p1", Int.MAX_VALUE)).current.pages.first().quarterTurns == 3) }
    scenario("duplicate retains source origin") {
        val p = base().dispatch(EditorAction.DuplicatePage("p2", "p4")).current.pages
        check(p.map { it.id } == listOf("p1", "p2", "p4", "p3") && p[2].sourcePageIndex == 1)
    }
    scenario("reject duplicate ID collision") { rejects<IllegalArgumentException> { base().dispatch(EditorAction.DuplicatePage("p1", "p2")) } }
    scenario("delete prunes selection") {
        val h = base().dispatch(EditorAction.SelectPages(setOf("p1", "p2"))).dispatch(EditorAction.DeletePages(setOf("p1")))
        check(h.current.selection.pageIds == setOf("p2") && h.current.pages.size == 2)
    }
    scenario("selection not undoable") { check(base().dispatch(EditorAction.SelectPages(setOf("p1"))).undoDepth == 1) }
    scenario("undo and redo") {
        val h = base().dispatch(EditorAction.MovePage("p1", 2))
        check(h.undo().current.pages.first().id == "p1")
        check(h.undo().redo().current.pages.last().id == "p1")
    }
    scenario("selection survives undo and redo when page exists") {
        val h = base().dispatch(EditorAction.SelectPages(setOf("p2"))).dispatch(EditorAction.MovePage("p1", 2))
        check(h.undo().current.selection.pageIds == setOf("p2"))
        check(h.undo().redo().current.selection.pageIds == setOf("p2"))
    }
    scenario("selection pruned on undo when page absent") {
        val h = base().dispatch(EditorAction.DuplicatePage("p1", "p4"))
            .dispatch(EditorAction.SelectPages(setOf("p4")))
        check(h.undo().current.selection.pageIds.isEmpty())
    }
    scenario("invalid source page count rejected") { rejects<IllegalArgumentException> { SourceDocumentRef("x", 0) } }
    scenario("new edit clears redo") {
        val h = base().dispatch(EditorAction.MovePage("p1", 2)).undo().dispatch(EditorAction.RotatePage("p1", 1))
        check(h.redoDepth == 0)
    }
    scenario("bounded history") {
        var h = EditorHistory.start(capacity = 2).dispatch(EditorAction.ImportSource(SourceDocumentRef("s1", 1), listOf("p1")))
        repeat(7) { h = h.dispatch(EditorAction.RotatePage("p1", 1)) }
        check(h.undoDepth == 2)
    }
    scenario("no-op does not grow history") { val h = base(); check(h.dispatch(EditorAction.MovePage("p1", 0)).undoDepth == h.undoDepth) }
    scenario("export plan respects reorder and rotation") {
        val h = base().dispatch(EditorAction.MovePage("p3", 0)).dispatch(EditorAction.RotatePage("p3", 1))
        val p = EditorExportPlan.from(h.current).pages
        check(p.map { it.sourcePageIndex } == listOf(2, 0, 1) && p.first().quarterTurns == 1)
    }
    scenario("reject empty export") { rejects<IllegalArgumentException> { EditorExportPlan.from(EditorDocumentState.empty()) } }
    scenario("selection copy isolation") {
        val input = mutableSetOf("p1")
        val h = base().dispatch(EditorAction.SelectPages(input))
        input.add("p2")
        check(h.current.selection.pageIds == setOf("p1"))
    }
    scenario("source and page list defensive copy") {
        val h = base()
        val pages = h.current.pages as MutableList<EditorPageRef>
        pages.clear()
        check(h.current.pages.size == 3)
    }
    scenario("invalid selection rejected") { rejects<IllegalArgumentException> { base().dispatch(EditorAction.SelectPages(setOf("missing"))) } }
    scenario("page source is opaque and stable") { check(base().current.pages.first().sourceId == "s1") }
    println("RESULT: $executed/$executed PASS (isolated Kotlin/JVM smoke only)")
}
