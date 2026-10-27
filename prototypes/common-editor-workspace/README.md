# Experimental common editor workspace — clean-room Kotlin PoC

**NOT INTEGRATED / NOT FINAL.** Independently authored platform-neutral Kotlin source and isolated JVM smoke harness. This prototype is **not** a trusted checkout, migrated product, Gradle/KMP build, Android/desktop integration, or production gate.

Run locally with a Kotlin compiler (this run used kotlinc-jvm 1.9.0 and JRE 21):

```sh
kotlinc prototypes/common-editor-workspace/src/commonMain/kotlin/org/embasic/pdfeditor/workspace/EditorWorkspace.kt \
  prototypes/common-editor-workspace/src/commonTest/kotlin/org/embasic/pdfeditor/workspace/EditorWorkspaceSmoke.kt \
  -include-runtime -d /tmp/embasic-workspace-smoke.jar
java -jar /tmp/embasic-workspace-smoke.jar
```

Domain-only source IDs are opaque and must be bound by a platform adapter to verified document bytes; export plans are declarative. No PDF engine, file access, renderer, Swing, Compose, Android URI, or `java.nio.Path` appears in commonMain. The history is bounded by snapshot count (1–128), not yet by a byte budget. This is a PoC, not an integrated application feature.

No GPL-3.0 PDF Arranger code or PRIVATE product implementation has been copied. Desktop PDFBox and Android PdfRenderer architecture remains unchanged. After secure source migration, strict dependency checks, trusted checkout, and real build baseline, reconcile this prototype against the canonical PUBLIC product module and write proper multiplatform tests before promoting it from `prototypes/` to product `commonMain`.
