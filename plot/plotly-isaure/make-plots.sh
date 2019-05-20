function make_plot {
  python3 SCRIPT-make-plot.py $tailstr $assemblyscheme $cutoff $axmax
  ascheme=`echo $assemblyscheme|sed 's/-/last/'`
  head=plots/$tailstr0-$ascheme-cutoff$cutoff-axmax$axmax
  \cp plotdata/data.csv $head.csv
  \cp plotdata/plotly.html $head.html
}

tailstr0=sum
tailstr=results-inc-ov-aa-sum
for assemblyscheme in -1 -2; do
  for cutoff in 2 3 5; do
    for axmax in 5 60 100; do
      make_plot
    done
  done
done

tailstr0=sumsum
tailstr=results-inc-ov-aa-sumsum
assemblyscheme=-1
for cutoff in 2 3 5; do
  for axmax in 5 60 100; do
    make_plot
  done
done
