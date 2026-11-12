package org.embasic.pdfeditor.platformtest

import android.app.Activity
import android.app.Instrumentation
import android.graphics.Bitmap
import android.graphics.Color
import android.graphics.Paint
import android.graphics.pdf.PdfDocument
import android.graphics.pdf.PdfRenderer
import android.os.Bundle
import android.os.ParcelFileDescriptor
import java.io.File
import java.io.FileOutputStream
import java.io.IOException

/**
 * ORIGINAL STAGING PROTOTYPE — Android platform APIs only, no JUnit or AndroidX test runner.
 * NOT compiled against Android SDK, NOT executed on an Android device, NOT a product module.
 * Requires an approved test APK, exact Gradle task, runner wiring and resolved license/NOTICE proof.
 */
class PlatformOnlyPdfInstrumentation : Instrumentation() {
    override fun onCreate(arguments: Bundle?) {
        super.onCreate(arguments)
        start()
    }

    override fun onStart() {
        val result = Bundle()
        var passed = 0
        var failed = 0
        var status = Activity.RESULT_CANCELED
        result.putString("v1121_protocol", "1")
        try {
            runSyntheticRenderAndPixelCheck()
            passed++
            runMalformedInputCheck()
            passed++
            status = Activity.RESULT_OK
            result.putString("v1121_outcome", "PASS")
        } catch (t: Throwable) {
            failed++
            // Exception class only; never log paths, file bytes, credentials or personal data.
            result.putString("v1121_outcome", "FAIL")
            result.putString("v1121_error_type", t.javaClass.simpleName.take(80))
        } finally {
            result.putInt("v1121_run", passed + failed)
            result.putInt("v1121_passed", passed)
            result.putInt("v1121_failed", failed)
            finish(status, result)
        }
    }

    private fun makeSyntheticPdf(): File {
        val file = File.createTempFile("embasic-v1121-", ".pdf", targetContext.cacheDir)
        val document = PdfDocument()
        try {
            val page = document.startPage(PdfDocument.PageInfo.Builder(96, 144, 1).create())
            val paint = Paint().apply { style = Paint.Style.FILL }
            paint.color = Color.WHITE
            page.canvas.drawRect(0f, 0f, 96f, 144f, paint)
            paint.color = Color.BLACK
            page.canvas.drawRect(32f, 56f, 64f, 88f, paint)
            document.finishPage(page)
            FileOutputStream(file).use { document.writeTo(it) }
            return file
        } catch (t: Throwable) {
            file.delete()
            throw t
        } finally {
            document.close()
        }
    }

    private fun runSyntheticRenderAndPixelCheck() {
        val file = makeSyntheticPdf()
        try {
            val descriptor = ParcelFileDescriptor.open(file, ParcelFileDescriptor.MODE_READ_ONLY)
            var renderer: PdfRenderer? = null
            try {
                renderer = PdfRenderer(descriptor) // renderer assumes ownership when constructed
                check(renderer.pageCount == 1) { "page count mismatch" }
                val page = renderer.openPage(0)
                try {
                    check(page.width == 96 && page.height == 144) { "wrong page geometry" }
                    val bitmap = Bitmap.createBitmap(96, 144, Bitmap.Config.ARGB_8888)
                    try {
                        bitmap.eraseColor(Color.MAGENTA) // unchanged output must not PASS
                        page.render(bitmap, null, null, PdfRenderer.Page.RENDER_MODE_FOR_DISPLAY)
                        val marker = luma(bitmap.getPixel(48, 72))
                        val background = luma(bitmap.getPixel(8, 8))
                        check(marker <= 80 && background >= 210 && background - marker >= 130) {
                            "rendered pixels differ from synthetic marker"
                        }
                    } finally { bitmap.recycle() }
                } finally { page.close() }
            } finally {
                if (renderer != null) renderer.close() else descriptor.close()
            }
        } finally {
            check(file.delete() || !file.exists()) { "synthetic cache PDF cleanup failed" }
        }
    }

    private fun runMalformedInputCheck() {
        val file = File.createTempFile("embasic-v1121-malformed-", ".pdf", targetContext.cacheDir)
        try {
            file.writeBytes("not-a-pdf".toByteArray(Charsets.US_ASCII))
            val descriptor = ParcelFileDescriptor.open(file, ParcelFileDescriptor.MODE_READ_ONLY)
            var renderer: PdfRenderer? = null
            var rejected = false
            try {
                try {
                    renderer = PdfRenderer(descriptor)
                } catch (_: IOException) { // a genuinely malformed PDF must be rejected by platform parser
                    rejected = true
                }
            } finally {
                if (renderer != null) renderer.close() else descriptor.close()
            }
            check(rejected) { "malformed input unexpectedly accepted" }
        } finally {
            check(file.delete() || !file.exists()) { "malformed cache PDF cleanup failed" }
        }
    }

    private fun luma(argb: Int): Int {
        check(Color.alpha(argb) >= 250) { "unexpected transparent output" }
        return (299 * Color.red(argb) + 587 * Color.green(argb) + 114 * Color.blue(argb) + 500) / 1000
    }
}
