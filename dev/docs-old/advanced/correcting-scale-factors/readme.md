# Correcting ABF Header Information

Sometimes ABFs get recorded with messed-up settings. I found this recently when current-clamp recordings were recorded with a voltage-clamp header. This made the units wrong and the scale factor wrong.

Header Variable | correct value | incorrect value
---|---|---
`StringsIndexed.lADCUnits` | `mV` | `pA`
`lDACChannelUnits[0]` | `pA` | `pA`
`ADCSection.fInstrumentScaleFactor` | `0.0005000000237487257` | `0.009999999776482582`

You can detect when an ABF file is screwed-up if `StringsIndexed.lADCUnits == lDACChannelUnits[0]`

After that, all that's required may be a correction of fInstrumentScaleFactor. In practice this is just off by a factor of 20.
