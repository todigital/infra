#!/usr/bin/perl

use vars qw/$libpath/;
use FindBin qw($Bin);
BEGIN { $libpath="$Bin" };
use lib "$libpath";
use lib "$libpath/../libs";

my @time = (localtime)[0..5];
my $Tdate = sprintf("%04d%02d%02d", $time[5]+1900, $time[4]+1, $time[3]);
my $Thour = sprintf("%02d", $time[2]);
my %dbconfig = loadconfig("/etc/apache2/infra.conf");
$curfetch = $dbconfig{curfetchua};
$limit = 20;

my $ps = `ps -xwww`;
$PARALLEL_STREAMS = 2;
@crawls = split(/batchconvertor\.pl/i, $ps);
$forbid = 1 if ($#crawls > $PARALLEL_STREAMS);
exit(0) if ($forbid);

use Getopt::Std;
%options=();
getopts("od:f:s:T",\%options);

# like the shell getopt, "d:" means d takes an argument
$file = $options{f} if defined $options{f};
$dir = $options{d} if defined $options{d};
$superdir = $options{s} if defined $options{s};
$options{T}++ unless (keys %options);
if ($options{T})
{
    $dir = "$curfetch/$Tdate/$Thour";
    push(@dirs, $dir);
    if ($Thour - 1 >= 0)
    {
        $Phour = sprintf("%02d", $Thour - 1);
        $dir = "$curfetch/$Tdate/$Phour";
        push(@dirs, $dir);
    }
    print "@dirs\n" if ($DEBUG);
}

foreach $dir (@dirs)
{
    opendir(DIR, $dir);
    @dir = readdir(DIR);

    foreach $file (@dir)
    {
	$skip = 0;
	$skip = 1 if ($file=~/(utf8|\.db|\.tmp)$/);
	$skip = 0 if (-e "$dir/$file.tmp");
	unless ($skip)
	{
	    print "$dir/$file\n" if ($DEBUG);
	    open(tmp, ">$dir/$file.tmp");
	    print tmp "\n";
	    close(tmp);
	    $convert = `$Bin/convert.py $dir/$file &`;
	    #unlink "$dir/$file.tmp";
	}
    }

}

sub loadconfig
{
    my ($configfile, $DEBUG) = @_;
    my %config;

    open(conf, $configfile);
    while (<conf>)
    {
        my $str = $_;
        $str=~s/\r|\n//g;
        my ($name, $value) = split(/\s*\=\s*/, $str);
        $config{$name} = $value;
    }
    close(conf);

    return %config;
}
