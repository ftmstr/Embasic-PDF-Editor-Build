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
    scenario("export omits completely deleted source") {
        val h = base()
            .dispatch(EditorAction.ImportSource(SourceDocumentRef("s2", 1), listOf("p4")))
            .dispatch(EditorAction.DeletePages(setOf("p1", "p2", "p3")))
        val plan = EditorExportPlan.from(h.current)
        check(plan.sources.map { it.id } == listOf("s2"))
        check(plan.pages.map { it.sourceId } == listOf("s2"))
    }
    scenario("export includes each referenced source once in import order") {
        val h = base()
            .dispatch(EditorAction.ImportSource(SourceDocumentRef("s2", 1), listOf("p4")))
            .dispatch(EditorAction.MovePage("p4", 0))
            .dispatch(EditorAction.DuplicatePage("p4", "p5"))
        val plan = EditorExportPlan.from(h.current)
        check(plan.sources.map { it.id } == listOf("s1", "s2"))
        check(plan.pages.map { it.sourceId } == listOf("s2", "s2", "s1", "s1", "s1"))
    }
    scenario("move selected nonadjacent pages to front preserving original order") {
        val h = base().dispatch(EditorAction.ImportSource(SourceDocumentRef("s2", 2), listOf("p4", "p5")))
            .dispatch(EditorAction.SelectPages(setOf("p2", "p4")))
            .dispatch(EditorAction.MovePages(setOf("p4", "p2"), 0))
        check(h.current.pages.map { it.id } == listOf("p2", "p4", "p1", "p3", "p5"))
        check(h.current.selection.pageIds == setOf("p2", "p4"))
    }
    scenario("move selected pages to end in reduced-list coordinates") {
        val h = base().dispatch(EditorAction.ImportSource(SourceDocumentRef("s2", 2), listOf("p4", "p5")))
            .dispatch(EditorAction.MovePages(setOf("p2", "p4"), 3))
        check(h.current.pages.map { it.id } == listOf("p1", "p3", "p5", "p2", "p4"))
        check(h.undo().current.pages.map { it.id } == listOf("p1", "p2", "p3", "p4", "p5"))
        check(h.undo().redo().current.pages.map { it.id } == listOf("p1", "p3", "p5", "p2", "p4"))
    }
    scenario("reject unknown page in multi-page move") {
        rejects<IllegalArgumentException> { base().dispatch(EditorAction.MovePages(setOf("p2", "missing"), 0)) }
    }
    scenario("reject empty multi-page move") {
        rejects<IllegalArgumentException> { base().dispatch(EditorAction.MovePages(emptySet(), 0)) }
    }
    scenario("reject multi-page insertion index outside reduced list") {
        rejects<IllegalArgumentException> { base().dispatch(EditorAction.MovePages(setOf("p1", "p3"), 2)) }
    }
    scenario("no-op multi-page move does not grow history") {
        val h = base()
        val moved = h.dispatch(EditorAction.MovePages(setOf("p1", "p2"), 0))
        check(moved.current.pages.map { it.id } == listOf("p1", "p2", "p3"))
        check(moved.undoDepth == h.undoDepth)
    }
    scenario("batch rotation updates selected pages atomically") {
        val h = base().dispatch(EditorAction.RotatePages(setOf("p1", "p3"), 1))
        check(h.current.pages.map { it.quarterTurns } == listOf(1, 0, 1))
        check(h.undoDepth == base().undoDepth + 1)
        check(h.undo().current.pages.map { it.quarterTurns } == listOf(0, 0, 0))
        check(h.undo().redo().current.pages.map { it.quarterTurns } == listOf(1, 0, 1))
    }
    scenario("batch rotation rejects unknown IDs without partial edit") {
        val h = base()
        rejects<IllegalArgumentException> { h.dispatch(EditorAction.RotatePages(setOf("p1", "missing"), 1)) }
        check(h.current.pages.all { it.quarterTurns == 0 })
    }
    scenario("batch rotation rejects empty page set") {
        rejects<IllegalArgumentException> { base().dispatch(EditorAction.RotatePages(emptySet(), 1)) }
    }
    scenario("batch rotation full turns is history no-op") {
        val h = base()
        val n = h.dispatch(EditorAction.RotatePages(setOf("p1", "p2"), Int.MIN_VALUE))
        check(n === h)
    }
    scenario("batch rotation preserves page order selection and export") {
        val h = base().dispatch(EditorAction.SelectPages(setOf("p2")))
            .dispatch(EditorAction.RotatePages(setOf("p3", "p1"), -1))
        check(h.current.pages.map { it.id } == listOf("p1", "p2", "p3"))
        check(h.current.selection.pageIds == setOf("p2"))
        check(EditorExportPlan.from(h.current).pages.map { it.quarterTurns } == listOf(3, 0, 3))
    }
    scenario("batch duplicate inserts copies after each original in document order") {
        val h = base().dispatch(EditorAction.DuplicatePages(linkedMapOf("p3" to "p5", "p1" to "p4")))
        check(h.current.pages.map { it.id } == listOf("p1", "p4", "p2", "p3", "p5"))
        check(h.current.pages.map { it.sourcePageIndex } == listOf(0, 0, 1, 2, 2))
        check(h.undoDepth == base().undoDepth + 1)
    }
    scenario("batch duplicate preserves source rotation selection and export plan") {
        val h = base().dispatch(EditorAction.RotatePages(setOf("p1", "p3"), 3))
            .dispatch(EditorAction.SelectPages(setOf("p1")))
            .dispatch(EditorAction.DuplicatePages(mapOf("p1" to "copy1", "p3" to "copy3")))
        check(h.current.selection.pageIds == setOf("p1"))
        check(h.current.pages.map { it.quarterTurns } == listOf(3, 3, 0, 3, 3))
        check(EditorExportPlan.from(h.current).pages.map { it.sourcePageIndex } == listOf(0, 0, 1, 2, 2))
        check(EditorExportPlan.from(h.current).sources.map { it.id } == listOf("s1"))
    }
    scenario("batch duplicate undo redo is atomic") {
        val h = base().dispatch(EditorAction.DuplicatePages(mapOf("p1" to "c1", "p2" to "c2")))
        check(h.undo().current.pages.map { it.id } == listOf("p1", "p2", "p3"))
        check(h.undo().redo().current.pages.map { it.id } == listOf("p1", "c1", "p2", "c2", "p3"))
    }
    scenario("batch duplicate rejects unknown origin and collisions without mutation") {
        val h = base()
        val bad = listOf(
            mapOf("p1" to "c1", "missing" to "c2"),
            mapOf("p1" to "p2"),
            mapOf("p1" to "c1", "p2" to "c1"),
            mapOf("p1" to ""),
        )
        for (mapping in bad) rejects<IllegalArgumentException> {
            h.dispatch(EditorAction.DuplicatePages(mapping))
        }
        check(h.current.pages.map { it.id } == listOf("p1", "p2", "p3"))
        check(h.undoDepth == 1)
    }
    scenario("batch duplicate rejects empty request") {
        rejects<IllegalArgumentException> { base().dispatch(EditorAction.DuplicatePages(emptyMap())) }
    }
    scenario("exhaustive five-page subset insertion preserves order and undo") {
        val initial = EditorHistory.start().dispatch(
            EditorAction.ImportSource(SourceDocumentRef("s1", 5), listOf("p1", "p2", "p3", "p4", "p5"))
        )
        val before = initial.current.pages.map { it.id }
        var cases = 0
        for (mask in 1 until (1 shl before.size)) {
            val moved = before.filterIndexed { index, _ -> mask and (1 shl index) != 0 }
            val remaining = before.filterNot { it in moved }
            for (target in 0..remaining.size) {
                val expected = remaining.take(target) + moved + remaining.drop(target)
                val result = initial.dispatch(EditorAction.MovePages(moved.toSet(), target))
                check(result.current.pages.map { it.id } == expected)
                check(result.current.pages.all { it.sourceId == "s1" })
                if (expected == before) check(result.undoDepth == initial.undoDepth)
                else {
                    check(result.undo().current.pages.map { it.id } == before)
                    check(result.undo().redo().current.pages.map { it.id } == expected)
                }
                cases++
            }
        }
        check(cases == 106) { "unexpected exhaustive case count: $cases" }
    }
    scenario("large import and selection preserve source identity and bounds") {
        val first = (0 until 4_000).map { "bulk-a-$it" }
        val second = (0 until 4_000).map { "bulk-b-$it" }
        val h = EditorHistory.start(capacity = 2)
            .dispatch(EditorAction.ImportSource(SourceDocumentRef("bulk-a", first.size), first))
            .dispatch(EditorAction.ImportSource(SourceDocumentRef("bulk-b", second.size), second))
            .dispatch(EditorAction.SelectPages((first + second).toSet()))
        check(h.current.pages.size == 8_000)
        check(h.current.pages.map { it.id }.toSet().size == 8_000)
        check(h.current.selection.pageIds.size == 8_000)
        check(h.current.pages.first().sourceId == "bulk-a")
        check(h.current.pages.last().sourceId == "bulk-b")
        check(h.undoDepth == 2)
        rejects<IllegalArgumentException> {
            h.dispatch(EditorAction.ImportSource(SourceDocumentRef("bulk-c", 1), listOf("bulk-a-1")))
        }
        rejects<IllegalArgumentException> { h.dispatch(EditorAction.SelectPages(setOf("not-in-document"))) }
    }
    scenario("large nonadjacent move retains order undo redo and rejects unknown IDs") {
        val ids = (0 until 10_000).map { "p-$it" }
        val original = EditorHistory.start(capacity = 2).dispatch(
            EditorAction.ImportSource(SourceDocumentRef("bulk", ids.size), ids)
        )
        val even = ids.filterIndexed { index, _ -> index % 2 == 0 }
        val odd = ids.filterIndexed { index, _ -> index % 2 != 0 }
        val moved = original.dispatch(EditorAction.MovePages(even.toSet(), 0))
        check(moved.current.pages.map { it.id } == even + odd)
        check(moved.undo().current.pages.map { it.id } == ids)
        check(moved.undo().redo().current.pages.map { it.id } == even + odd)
        check(EditorExportPlan.from(moved.current).pages.size == ids.size)
        rejects<IllegalArgumentException> {
            original.dispatch(EditorAction.MovePages(even.toSet() + "missing", 0))
        }
        rejects<IllegalArgumentException> {
            original.dispatch(EditorAction.MovePages(even.toSet(), odd.size + 1))
        }
    }
    scenario("10k page batch rotate select delete membership preserves semantics") {
        val ids = (0 until 10_000).map { "stress-$it" }
        val all = ids.toSet()
        val initial = EditorHistory.start(capacity = 4).dispatch(
            EditorAction.ImportSource(SourceDocumentRef("stress-source", ids.size), ids)
        )
        val selected = initial.dispatch(EditorAction.SelectPages(all))
        check(selected.current.selection.pageIds == all)
        check(selected.undoDepth == initial.undoDepth)
        val rotated = selected.dispatch(EditorAction.RotatePages(all, 1))
        check(rotated.current.pages.all { it.quarterTurns == 1 })
        check(rotated.undo().current.pages.all { it.quarterTurns == 0 })
        check(rotated.undo().redo().current.pages.all { it.quarterTurns == 1 })
        val evens = ids.filterIndexed { index, _ -> index % 2 == 0 }.toSet()
        val deleted = rotated.dispatch(EditorAction.DeletePages(evens))
        check(deleted.current.pages.size == 5_000)
        check(deleted.current.selection.pageIds == all - evens)
        check(deleted.current.pages.all { it.quarterTurns == 1 })
        check(EditorExportPlan.from(deleted.current).pages.size == 5_000)
        check(deleted.undo().current.pages.size == 10_000)
        for (invalid in listOf(
            EditorAction.RotatePages(setOf("missing"), 1),
            EditorAction.DeletePages(setOf("missing")),
            EditorAction.SelectPages(setOf("missing")),
        )) rejects<IllegalArgumentException> { initial.dispatch(invalid) }
    }
    scenario("selected export preserves document order across sources") {
        val h = base().dispatch(EditorAction.ImportSource(SourceDocumentRef("s2", 2), listOf("p4", "p5")))
            .dispatch(EditorAction.MovePage("p4", 0))
            .dispatch(EditorAction.SelectPages(linkedSetOf("p3", "p4", "p1")))
        val plan = EditorExportPlan.fromSelection(h.current)
        check(plan.pages == listOf(EditorExportPage("s2", 0, 0), EditorExportPage("s1", 0, 0), EditorExportPage("s1", 2, 0)))
        check(plan.sources == listOf(SourceDocumentRef("s1", 3), SourceDocumentRef("s2", 2)))
    }
    scenario("selected export excludes unselected sources and pages") {
        val h = base().dispatch(EditorAction.ImportSource(SourceDocumentRef("private-unselected", 1), listOf("p4")))
            .dispatch(EditorAction.SelectPages(setOf("p2")))
        val plan = EditorExportPlan.fromSelection(h.current)
        check(plan.pages == listOf(EditorExportPage("s1", 1, 0)))
        check(plan.sources == listOf(SourceDocumentRef("s1", 3)))
    }
    scenario("selected export retains separately rotated duplicate origins") {
        val h = base().dispatch(EditorAction.DuplicatePage("p1", "copy"))
            .dispatch(EditorAction.RotatePage("p1", 1))
            .dispatch(EditorAction.RotatePage("copy", -1))
            .dispatch(EditorAction.SelectPages(setOf("copy", "p1")))
        check(EditorExportPlan.fromSelection(h.current).pages == listOf(EditorExportPage("s1", 0, 1), EditorExportPage("s1", 0, 3)))
    }
    scenario("empty selection fails closed even in a nonempty document") {
        rejects<IllegalArgumentException> { EditorExportPlan.fromSelection(base().current) }
        rejects<IllegalArgumentException> { EditorExportPlan.fromSelection(EditorDocumentState.empty()) }
    }
    scenario("selected export snapshot survives later edits and defensive copy attempts") {
        val h = base().dispatch(EditorAction.SelectPages(setOf("p1", "p2")))
        val plan = EditorExportPlan.fromSelection(h.current)
        val later = h.dispatch(EditorAction.RotatePage("p1", 1)).dispatch(EditorAction.DeletePages(setOf("p2")))
        (plan.pages as MutableList<EditorExportPage>).clear()
        check(plan.pages == listOf(EditorExportPage("s1", 0, 0), EditorExportPage("s1", 1, 0)))
        check(EditorExportPlan.fromSelection(later.current).pages == listOf(EditorExportPage("s1", 0, 1)))
        check(h.current.selection.pageIds == setOf("p1", "p2"))
    }
    scenario("whole export remains independent of selection and select-all matches it") {
        val h = base().dispatch(EditorAction.SelectPages(setOf("p2")))
        check(EditorExportPlan.from(h.current).pages.size == 3)
        val all = h.dispatch(EditorAction.SelectPages(setOf("p1", "p2", "p3")))
        val extracted = EditorExportPlan.fromSelection(all.current)
        check(extracted.pages == EditorExportPlan.from(all.current).pages)
        check(extracted.sources == EditorExportPlan.from(all.current).sources)
    }
    scenario("selected export does not mutate history and rejects selection pruned by undo") {
        val h = base().dispatch(EditorAction.DuplicatePage("p1", "copy"))
            .dispatch(EditorAction.SelectPages(setOf("copy")))
        val depth = h.undoDepth
        EditorExportPlan.fromSelection(h.current)
        check(h.undoDepth == depth && h.redoDepth == 0 && h.current.pages.size == 4)
        rejects<IllegalArgumentException> { EditorExportPlan.fromSelection(h.undo().current) }
    }
    scenario("10k page selective extract includes exactly the requested 5k pages") {
        val ids = (0 until 10_000).map { "extract-$it" }
        val selected = ids.filterIndexed { index, _ -> index % 2 == 1 }.reversed().toSet()
        val h = EditorHistory.start(capacity = 2)
            .dispatch(EditorAction.ImportSource(SourceDocumentRef("bulk", ids.size), ids))
            .dispatch(EditorAction.SelectPages(selected))
        val plan = EditorExportPlan.fromSelection(h.current)
        check(plan.pages.map { it.sourcePageIndex } == (1 until 10_000 step 2).toList())
        check(plan.sources == listOf(SourceDocumentRef("bulk", 10_000)))
        check(h.current.pages.size == 10_000)
    }
    println("RESULT: $executed/$executed PASS (isolated Kotlin/JVM smoke only)")
}
