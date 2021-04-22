import shutit
import os

shutit.pane()

# https://asciinema.org/a/140690

# The gnuplot prompt to expect.
gnuplot_expect='gnuplot> '

# Create a bash session.
s = shutit.create_session(loglevel='warning',video=2)

# If gnuplot is not installed, install it.
if s.send_and_get_output('which gnuplot') == '':
	s.install('gnuplot')

# Ensure we are in this script's folder.
s.send('cd ' + os.path.dirname(os.path.realpath(__file__)))

# Gnuplot session.
s.send('gnuplot',expect=gnuplot_expect,note='Start gnuplot')
s.send('set terminal png',expect=gnuplot_expect,note='Set the terminal to output png files.')
s.send('set style line 1',expect=gnuplot_expect,note='Set the style to a line')
s.send('set xdata time',expect=gnuplot_expect,note='Identify the x axis as of the "time" type')
s.send('set xlabel "Month"',expect=gnuplot_expect,note='Set the label for the x axis to read "Month"')
s.send('set ylabel "GBPpm, 12mth RA"',expect=gnuplot_expect,note='Set the labe for the t axis')
s.send('set xtics rotate',expect=gnuplot_expect,note='Rotate the x axis labels by 90 degrees')
s.send('set timefmt "%Y-%m"',expect=gnuplot_expect,note='Tell gnuplot the date format in the file')
s.send("set output 'dividends.png'",expect=gnuplot_expect,note='Set the output file name')
s.send("plot 'dividend_12mth.dat' using 2:1 with lines",expect=gnuplot_expect,note='Draw the graph, indicating the file, and the x/y columes. Draw the graph with a line.')
s.send('exit',note='Exit gnuplot')
if s.get_os() == 'osx':
	s.send('open dividends.png')
else:
	s.send('display dividends.png')
