> ## WARNING: INCOMPLETE CONTENT
> This document is a work in progress. Until it is complete, refer to the [old version](../) of this document.

---

# Unofficial Guide to the ABF File Format

***by [Scott Harden](http://www.SWHarden.com)***

The field of cellular electrophysiology uses highly-sensitive voltage and current measurement devices to gain insights into the electrical properties of biological membranes. Voltage-clamp and current-clamp circuits are used to measure the flow of ions through ion channels embedded in small patches of cell membembranes. This technique is called _patch-clamp electrophysiology_, and Axon Instruments (now a division of Molecular Devices) sells patch-clamp systems (including amplifiers, digitizers, and software) which are commonly used by electrophysiologists in scientific research environments. Electrophysiological data produced by theses systems is saved in Axon Binary Format (ABF) files. Their patch-clamp analysis software suite (pClamp) includes acquisition software (Clampex) and analysis software (ClampFit) which can read and write ABF files.

Axon Binary Format (ABF) files are encoded in a proprietary format. In the early 2000s the internal file structure of ABF1 files was widely understood and data could be easily read from ABF1 files. In 2006 pCLAMP 10 was released, featuring a new file format (ABF2) which was intentionally undocumented. Programmers seeking to write software to analyze ABF files were encouraged to interact with ABF files exclusively through a 32-bit Windows-only DLL they provide (without source code) as part of the Axon pCLAMP SDK.

>According to the [official documentation](https://mdc.custhelp.com/euf/assets/content/ABFHelp.pdf): "_One of the goals of the ABF reading routines is to isolate the applications programmer from the need to know anything other than the most basic information about the file format. ABF 2.0 now uses a header of variable length.  This means that it is now essential to use the ABFFIO.DLL library to access the data._"
