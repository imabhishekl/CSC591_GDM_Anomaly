Team members:

     Name        |  Unity ID
-----------------------------
Abhishek Lingwal    aslingwa
Shruti Kuber        skuber
Raunaq Saxena       rsaxena

Python Libraries Prerequisite:
numpy, scipy, networkx

Command to execute:

python anomaly.py <path_to_directory>

Eg:

python anomaly.py /home/jdoe/sampledir/

Output:

sampledir_time_series.txt - containing similarity values of each adjacent graph


Results explanation:
We were able to generate the output data and plots for 3 datasets and partial output, 
ie, similarity of the first 6 pairs of p2p-Gnutella graph. Post using sparse matrix the p2p-
Gnutella dataset was taking above 3 hours to execute, thus we decided to display the partial result,
excluding the last two pairs.

The autonomous dataset showcased some anomalies where as we didn't find any anomalies in the voice and
enron dataset.

The lower threshold value that is used to detect anomalies, although maybe accurate, but for cases where
number of graphs aren't a lot or if not too many edges in general, detecting an anomaly would have a low
possibility on approximating the math as the moving range values would be large enough to move the value below
nearly every reported value.
