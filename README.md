### HPV-detekcija

Programa, skirta atrinkti probių rinkinį tam tikrų virusų DNR detekcijai. Pritikyta žmogaus papilomos viruso (HPV) 16,18,31,33,35 tipų (sukelia gimdos kaklelio vėžį) infekcijai nustatyti.

Diagnostinė sistema specifiška ir turi nebūti signalo nepavojingų HPV infekcijų atvejais (tipai 6, 11, 40, 42, 43, 44).

### Algoritmas

1. Parsiųsta visų tipu pavojingų ir nepavojingų zmogaus papilomos viruso prieinamos sekos fasta formatu, naudojant blast paiešką. Panaikintos identiškos sekos. Naudojant mafft sudarytas sekų palyginys, kai failo viršuje pavojingi tipai, o žemiau nepavojingi. 

2. Parinkti probių sistemą pavojingų papilomos viruso tipų detekcijai, kurioje būtų kuo mažiau probių kiekis tinkantis visų žinomų didelės rizikos HPV tipų variantų diagnostikai, taip kad:

 Visų probių ilgis 30 bazių porų (bp). Probė – tai trumpas DNR fragmentas, DNR sekos intervalas.
 Kiekvienai didelio pavojingumo papilomos viruso sekai yra bent po vieną probę rinkinyje, taip kad tarp jos sekos ir viruso sekos būtų ne daugiau nei 2 nesutapimai.
 Visos probės turi bent po 3 nesutapimus su visomis nepavojingų virusų sekomis.
 DNR sekos sritis, iš kurio parenkamos visos probės neilgesnės nei 60 bp.


