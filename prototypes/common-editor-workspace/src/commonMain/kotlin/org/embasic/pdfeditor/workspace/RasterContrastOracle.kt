package org.embasic.pdfeditor.workspace

/** Original platform-neutral ARGB sample; the platform adapter must supply pixels from a real render. */
data class RasterPixelSample(val x: Int, val y: Int, val argb: Int)

data class RasterContrastEvidence(val darkLuma: Int, val lightLuma: Int, val contrast: Int)

/**
 * A limited PDF raster acceptance oracle, not a renderer or an authentication of sample provenance.
 * The adapter must sample the *actual* bitmap after rendering and must not generate fake samples.
 * Sampling two non-edge points never proves every PDF feature or page is correctly rasterized.
 */
object RasterContrastOracle {
    private const val MAX_PIXELS = 16_777_216L

    fun verify(
        width: Int,
        height: Int,
        expectedDark: RasterPixelSample,
        expectedLight: RasterPixelSample,
    ): RasterContrastEvidence {
        require(width > 0 && height > 0 && width.toLong() * height.toLong() <= MAX_PIXELS) {
            "unsafe bitmap dimensions"
        }
        fun checkPoint(p: RasterPixelSample) {
            require(p.x in 0 until width && p.y in 0 until height) { "sample outside bitmap" }
            require((p.argb ushr 24) >= 250) { "sample must be opaque" }
        }
        checkPoint(expectedDark)
        checkPoint(expectedLight)
        require(expectedDark.x != expectedLight.x || expectedDark.y != expectedLight.y) {
            "sample locations must differ"
        }
        fun luma(argb: Int): Int {
            val red = (argb ushr 16) and 0xFF
            val green = (argb ushr 8) and 0xFF
            val blue = argb and 0xFF
            return (299 * red + 587 * green + 114 * blue + 500) / 1000
        }
        val dark = luma(expectedDark.argb)
        val light = luma(expectedLight.argb)
        val difference = light - dark
        require(dark <= 80 && light >= 210 && difference >= 130) {
            "wrong/blank/unrendered PDF raster samples"
        }
        return RasterContrastEvidence(dark, light, difference)
    }
}
