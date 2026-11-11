package org.embasic.pdfeditor.workspace

/** Independent stdlib-only smoke tests, not Android or Gradle product tests. */
private var passed = 0
private fun test(name: String, body: () -> Unit) { body(); passed++; println("PASS $name") }
private inline fun <reified T: Throwable> reject(noinline action: () -> Unit) {
    try { action() } catch (x: Throwable) { if (x is T) return; throw x }
    error("expected rejection: ${T::class.simpleName}")
}
private fun pix(x: Int, y: Int, rgb: Int) = RasterPixelSample(x, y, rgb)
private val BLACK = 0xFF000000.toInt()
private val WHITE = 0xFFFFFFFF.toInt()
private val MAGENTA = 0xFFFF00FF.toInt()
private fun verify(dark: RasterPixelSample = pix(48, 72, BLACK),
                   light: RasterPixelSample = pix(8, 8, WHITE),
                   width: Int = 96, height: Int = 144): RasterContrastEvidence =
    RasterContrastOracle.verify(width, height, dark, light)
fun main() {
    test("black marker white background passes") { check(verify().contrast >= 200) }
    test("blank image rejected") { reject<IllegalArgumentException> { verify(dark = pix(48, 72, WHITE)) } }
    test("both black rejected") { reject<IllegalArgumentException> { verify(light = pix(8, 8, BLACK)) } }
    test("swapped contrast rejected") { reject<IllegalArgumentException> { verify(dark = pix(48, 72, WHITE), light = pix(8, 8, BLACK)) } }
    test("unrendered magenta rejected") { reject<IllegalArgumentException> { verify(dark = pix(48, 72, MAGENTA), light = pix(8, 8, MAGENTA)) } }
    test("transparent black rejected") { reject<IllegalArgumentException> { verify(dark = pix(48, 72, 0x00000000)) } }
    test("transparent white rejected") { reject<IllegalArgumentException> { verify(light = pix(8, 8, 0x00FFFFFF)) } }
    test("dark out of bounds rejected") { reject<IllegalArgumentException> { verify(dark = pix(96, 72, BLACK)) } }
    test("light negative coordinate rejected") { reject<IllegalArgumentException> { verify(light = pix(-1, 8, WHITE)) } }
    test("coincident sample locations rejected") { reject<IllegalArgumentException> { verify(light = pix(48, 72, WHITE)) } }
    test("zero extent rejected") { reject<IllegalArgumentException> { verify(width = 0) } }
    test("integer overflow dimensions rejected") { reject<IllegalArgumentException> { verify(width = Int.MAX_VALUE, height = Int.MAX_VALUE) } }
    test("low contrast grayscale rejected") { reject<IllegalArgumentException> { verify(dark = pix(48, 72, 0xFF777777.toInt()), light = pix(8, 8, 0xFF888888.toInt())) } }
    test("anti-aliased non-edge interior passes") { check(verify(dark = pix(48, 72, 0xFF171717.toInt()), light = pix(8, 8, 0xFFF7F7F7.toInt())).contrast >= 200) }
    test("deterministic adversarial grayscale 4000 variants") {
        for (i in 0 until 4_000) {
            val gray = i % 256
            val c = (0xFF000000L or (gray.toLong() shl 16) or (gray.toLong() shl 8) or gray.toLong()).toInt()
            reject<IllegalArgumentException> { verify(dark = pix(48, 72, c), light = pix(8, 8, c)) }
        }
    }
    println("TOTAL $passed/15 PASS")
}
