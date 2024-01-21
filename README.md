### HPV-detekcija

Programa, skirta atrinkti probių rinkinį tam tikrų virusų DNR detekcijai. Pritikyta žmogaus papilomos viruso (HPV) 16,18,31,33,35 tipų (sukelia gimdos kaklelio vėžį) infekcijai nustatyti.

Diagnostinė sistema specifiška ir neturi signalo nepavojingų HPV infekcijų atvejais (tipai 6, 11, 40, 42, 43, 44).

### Algoritmas

1. Parsiųstos visų tipu pavojingų ir nepavojingų žmogaus papilomos viruso prieinamos sekos fasta formatu, naudojant blast paiešką. Panaikintos identiškos sekos. Naudojant mafft serverį sudarytas sekų palyginys, kai failo viršuje pavojingi tipai, o žemiau nepavojingi. 

2. Parinkta probių sistema pavojingų papilomos viruso tipų detekcijai, kurioje kuo mažesnis probių kiekis tinkantis visų žinomų didelės rizikos HPV tipų variantų diagnostikai, taip kad:

 Visų probių ilgis 30 bazių porų (bp). Probė – tai trumpas DNR fragmentas, DNR sekos intervalas. <br>
 Kiekvienai didelio pavojingumo papilomos viruso sekai yra bent po vieną probę rinkinyje, taip kad tarp jos sekos ir viruso sekos būtų `ne daugiau nei 2 nesutapimai`. <br>
 Visos probės turi bent po 3 nesutapimus su visomis nepavojingų virusų sekomis. <br>
 DNR sekos sritis, iš kurio parenkamos visos probės neilgesnės nei 60 bp. <br>


