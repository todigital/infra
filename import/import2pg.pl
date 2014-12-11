#!/usr/bin/perl

use vars qw/$libpath/;
use FindBin qw($Bin);
BEGIN { $libpath="$Bin" };
use lib "$libpath";
use lib "$libpath/../libs";

use DB_File;
use DBI;
use Encode;
use Lingua::DetectCharset;
$| = 1;
use Try::Tiny;

use Getopt::Std;
%options=();
getopts("od:f:s:T",\%options);

my @time = (localtime)[0..5];
my $Tdate = sprintf("%04d%02d%02d", $time[5]+1900, $time[4]+1, $time[3]);
my $Thour = sprintf("%02d", $time[2]);
my %dbconfig = loadconfig("/etc/apache2/infra.conf");
$curfetch = $dbconfig{curfetchua};
$limit = 60;

# like the shell getopt, "d:" means d takes an argument
$file = $options{f} if defined $options{f};
$dir = $options{d} if defined $options{d};
$superdir = $options{s} if defined $options{s};
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
	if ($file=~/\.utf8$/)
	{
	    $dbfile = "$dir/$file.db";
	    my $newfileflag = 1;

	    $indatabase{"$dir/$file"} = "$dbfile";
	    $newfileflag = 0 if (-e $indatabase{"$dir/$file"});
	    $newfileflag = 0 if ($files >= $limit);
	    if ($newfileflag)
	    {
	        $path = "$dir/$file";
	        push(@files, "$path");
		$files++;
	    }
	};
    }
    closedir(DIR);
}

foreach $file (@files)
{
    if ($file=~/\/(\d{4})(\d{2})(\d{2})\/(\d+)/)
    {
        my $date = sprintf("%04d-%02d-%02d %02d:00", $1, $2, $3, $4);
	$hour = $4;
        $dates{$file} = $date;
    }

    print "$file\n" if ($DEBUG);
    my ($charset, $url, $root, $title, $html, $content, $text) = readhtml($file);
    print "$url\n";
    $title = $dbh->quote($title);
    $html = $dbh->quote($html);  
    $content = $dbh->quote($content);
    $text = $dbh->quote($text);
    $id = '0';
    $true = 0;
    $true = 1 if ($url && !$known{$url}); # && $charset=~/utf/i);
    $true = 0 if ($url=~/(\.jpg|\.png)/sxi);
    $true = 0 unless ($charset);

    if ($true)
    {
        $sql = "insert into news (filename, charset, hour, title, html, content, text, url, root, founddate) values ('$file', '$charset', '$hour', $title, $html, $content, $text, '$url', '$root', '$dates{$file}');";
	try {
		$dbh->do($sql);
		open(status, ">$indatabase{$file}");
		print status "$url\n$title\n";
	 	close(status);
	} catch {
		warn "error: $url\n";
	}
	#print "$sql\n";
    }
    $known{$url}++;
}

sub readhtml
{
    my ($filename, $DEBUG) = @_;
    my ($title, $root, $html, $text);

    print "READ $filename\n";
    open(smfile, $filename);
    @content = <smfile>;
    close(smfile);
    my $texthtml = '';
    
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
    $text = $html;
    $content = $html; 
    #$content=~s/<(?:[^>'"]*|(['"]).*?\1)*>//gsx;
    $text =~ s/<script.*?<\'/script>/sg;
    $text =~ s/<.+?>//sg;

    #print "$title\n";
    if ($DEBUG)
    {
        #print  "@content\n";
        print "$title\n";
        print "$content\n";
    };

    $charset = 'utf8';
    return ($charset, $url, $root, $title, $html, $content, $text);
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
