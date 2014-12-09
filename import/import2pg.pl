#!/usr/bin/perl

use vars qw/$libpath/;
use FindBin qw($Bin);
BEGIN { $libpath="$Bin" };
use lib "$libpath";
use lib "$libpath/../libs";

use DB_File;
use DBI;
$| = 1;

use Getopt::Std;
%options=();
getopts("od:f:s:",\%options);
# like the shell getopt, "d:" means d takes an argument
$file = $options{f} if defined $options{f};
$dir = $options{d} if defined $options{d};
$superdir = $options{s} if defined $options{s};

my %dbconfig = loadconfig("/etc/apache2/infra.conf");
$site = $dbconfig{root};
my ($dbname, $dbhost, $dblogin, $dbpassword) = ($dbconfig{dbname}, $dbconfig{dbhost}, $dbconfig{dblogin}, $dbconfig{dbpassword});
my $dbh = DBI->connect("dbi:Pg:dbname=$dbname;host=$dbhost",$dblogin,$dbpassword,{AutoCommit=>1,RaiseError=>1,PrintError=>0});

push(@files, $file) if ($file);
push(@dirs, $dir) if ($dir);
if ($superdir)
{
    opendir(DIR, $superdir);
    @dir = readdir(DIR);
    foreach $thisdir (@dir)
    {
        if (-d "$superdir/$thisdir")
        {
	    if ($thisdir=~/\w+/)
	    {
                push(@dirs, "$superdir/$thisdir");
	    };
        }
    }
    closedir(DIR);
}

foreach $dir (@dirs)
{
    opendir(DIR, $dir);
    @dir = readdir(DIR);
    foreach $file (@dir)
    {
	if ($file=~/\w+/ && $file!~/\.start/)
	{
	    push(@files, "$dir/$file");
	}
    }
    closedir(DIR);
}

foreach $file (@files)
{
    print "$file\n";
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
