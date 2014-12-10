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
	if ($file=~/\w+/ && $file!~/(\.start|\.bak|\.orig)/)
	{
	    $path = "$dir/$file";
	    #$convert = `$Bin/convert.py $dir/$file`;
	    push(@files, "$path");
	}
	if ($file=~/\.bak/)
	{
	    $ofile = $file;
	    $ofile=~s/\.bak//g;
	    $mv = `/bin/mv $dir/$file $dir/$ofile`;
	    print "$dir/$file\n";
	}
    }
    closedir(DIR);
}

foreach $file (@files)
{
    if ($file=~/\/(\d{4})(\d{2})(\d{2})\/(\d+)/)
    {
        my $date = sprintf("%04d-%02d-%02d %02d:00", $1, $2, $3, $4);
        $dates{$file} = $date;
    }

    print "$file\n" if ($DEBUG);
    my ($url, $root, $title, $html, $content, $text) = readhtml($file);
    print "$url\n";
    $title = $dbh->quote($title);
    $html = $dbh->quote($html);  
    $content = $dbh->quote($content);
    $text = $dbh->quote($text);
    $id = '0';
    if ($url && !$known{$url})
    {
        $sql = "insert into news (title, html, content, text, url, root, founddate) values ($title, $html, $content, $text, '$url', '$root', '$dates{$file}');";
	$dbh->do($sql);
	#print "$sql\n";
    }
    $known{$url}++;
}

sub readhtml
{
    my ($filename, $DEBUG) = @_;
    my ($title, $root, $html, $text);

    $convert = `$Bin/convert.py $filename`;
    print "READ $filename\n";
    open my $fh, "<:encoding(utf8)", $filename or die "$filename\n";
    binmode STDOUT, ':utf8';
    @content = <$fh>;
    close $fh;

    $url = shift @content;
    if ($url=~/Monitorix\-url\:\s+(.+)/)
    {
	$url=$1;
	if ($url=~/^(http\:\/\/\S+?)\//)
	{
	   $root = $1;
	}
    }

    $html = "@content";
    if ($html=~/<title>(.+?)(<\/title>)/sxi)
    {
	$title = $1;
    }
    $title = "notitle" unless ($title);
    $text = $title;
    $content = $html; 
    #$content=~s/<(?:[^>'"]*|(['"]).*?\1)*>//gsx;
    print "$title\n";
    if ($DEBUG)
    {
    #print  "@content\n";
    print "$title\n";
    print "$content\n";
    };

    #print "$url $root\n";
    #print "$filename\n";
    return ($url, $root, $title, $html, $content, $text);
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
