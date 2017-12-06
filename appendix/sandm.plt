set term aqua enhanced font "Times-Roman, 18" dashed
set datafile separator ","
set xlabel 'y[m]'
set xrange [625:5000]
set ylabel 'S[N] and M[Nm]'
plot 'sm_graph.csv' using 1:12  w lines dt 3 linecolor rgb 'black' ti "S"
replot 'sm_graph.csv' using 1:13 w lines lt 2 linecolor rgb 'black'ti "M"
