### HPV-detekcija

Programa, skirta atrinkti probių rinkinį tam tikrų virusų DNR detekcijai. Pritikyta žmogaus papilomos viruso (HPV) 16,18,31,33,35 tipų (sukelia gimdos kaklelio vėžį) infekcijai nustatyti.

Diagnostinė sistema specifiška ir neturi signalo nepavojingų HPV infekcijų atvejais (tipai 6, 11, 40, 42, 43, 44).

### Algoritmas

1. Parsiųstos visų tipu pavojingų ir nepavojingų žmogaus papilomos viruso prieinamos sekos fasta formatu, naudojant blast paiešką. Panaikintos identiškos sekos. Naudojant mafft serverį sudarytas sekų palyginys, kai failo viršuje pavojingi tipai, o žemiau nepavojingi. 

2. Parinkta probių sistema pavojingų papilomos viruso tipų detekcijai, kurioje kuo mažesnis probių kiekis tinkantis visų žinomų didelės rizikos HPV tipų variantų diagnostikai, taip kad:

 Visų probių ilgis `30 bazių porų` (bp). Probė – tai trumpas DNR fragmentas, DNR sekos intervalas. <br>
 Kiekvienai didelio pavojingumo papilomos viruso sekai yra bent po vieną probę rinkinyje, taip kad tarp jos sekos ir viruso sekos būtų `ne daugiau nei 2 nesutapimai`. <br>
 Visos probės turi `bent po 3 nesutapimus` su visomis nepavojingų virusų sekomis. <br>
 DNR sekos sritis, iš kurio parenkamos visos probės neilgesnės nei `60 bp`. <br>

3. Kadangi reikia analizuoti `didelį kiekį duomenų`, pasinaudota dalykinės srities žiniomis, bandant sumažinti probių ieškojimo sritį. Apskaičiuota `60 bp` regionų konservatyvumas naudojantis entropijos formule. Didžiausią konservatyvumą turintys regionai greičiausiai yra virusui funkciškai svarbiausi ir mažai kintantys t.y sritys, leidžiančios atpažinti pavojingus virusus.

### HPV Detection
A program designed to select a set of samples for the detection of certain viruses' DNA. It is approved for detecting infections caused by human papillomavirus (HPV) types 16, 18, 31, 33, 35 (which cause cervical cancer).

The diagnostic system is specific and does not signal non-threatening HPV infections (types 6, 11, 40, 42, 43, 44).

### Algorithm
1. All available sequences of both dangerous and non-dangerous human papillomavirus types are downloaded in fasta format and searched using BLAST. Identical sequences are removed. A sequence alignment is created using the MAFFT server, with dangerous types at the top of the file and non-dangerous types below.

2. A probe system is selected for the detection of dangerous papillomavirus types, with the aim of using the smallest amount of probes suitable for diagnosing all known high-risk HPV type variants, so that:

The length of all probes is `30 base pairs (bp)`. A probe is a short DNA fragment, an interval of DNA sequences. <br>
For each high-risk papillomavirus sequence, there is at least one probe in the set, so that there are `no more than 2 mismatches` between its sequence and the virus sequence. <br>
All probes have `at least 3 mismatches` with all non-dangerous virus sequences. <br>
The DNA sequence regions from which all probes are selected are no shorter than `60 bp`. <br>

3. Since a `large amount of data` needs to be analyzed, domain knowledge has been used to reduce the search area for probes. The conservatism of `60 bp` regions was calculated using the entropy formula. The regions with the highest conservatism are likely to be functionally important to the virus and less variable, i.e., regions that allow the identification of dangerous viruses.


