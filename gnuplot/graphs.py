import shutit
import os

# The gnuplot prompt to expect.
gnuplot_expect='gnuplot> '

# Create a bash session.
s = shutit.create_session(loglevel='warning',walkthrough=True)

# If gnuplot is not installed, install it.
if s.send_and_get_output('which gnuplot') == '':
	s.install('gnuplot')

# Ensure we are in this script's folder.
s.send('cd ' + os.path.dirname(os.path.realpath(__file__)))

# Gnuplot session.
s.send('gnuplot',expect=gnuplot_expect)
s.send('set terminal png',expect=gnuplot_expect)
s.send('set style line 1 lc rgbcolour black',expect=gnuplot_expect)
s.send('set xdata time',expect=gnuplot_expect)
s.send('set xlabel "month"',expect=gnuplot_expect)
s.send('set xtics rotate',expect=gnuplot_expect)
s.send('set ylabel "GBPpm, 12mth RA"',expect=gnuplot_expect)
s.send('set timefmt "%Y-%m"',expect=gnuplot_expect)
s.send("set output 'dividends.png'",expect=gnuplot_expect)
s.send("plot 'dividend_12mth.dat' using 2:1 with lines",expect=gnuplot_expect)
s.send("exit")
s.send("display dividends.png")
