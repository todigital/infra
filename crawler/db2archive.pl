#!/usr/bin/perl

my @time = (localtime)[0..5];
my $pdate = sprintf("%04d-%02d-%02d", $time[5]+1900, $time[4]+1, $time[3]);
my $date = sprintf("%04d-%02d-%02d", $time[5]+1900, $time[4]+1, $time[3]);

use vars qw/$libpath/;
use FindBin qw($Bin);
BEGIN { $libpath="$Bin" };
use lib "$libpath";
use lib "$libpath/../../monitorix.spider/libs";
use lib "$libpath/../../ua/monitorix/libs";
use Configall;
use DBI;
my ($mainworkdir, %conf) = config("$Bin/../../ua/monitorix/config");

my ($data_dbname, $data_dbhost, $data_dbuser, $data_dbpasswd) = ($conf{spider_db}, $conf{spider_host}, $conf{spider_user}, $conf{spider_passwd});

$dbh = DBI->connect("DBI:mysql:$data_dbname:$data_dbhost", "$data_dbuser", "$data_dbpasswd") or warning("$!");
$dbh->do("set names utf8");

if ($dbh)
{
    $sql1 = "insert into archive select * from spider_info where insertdate < '$date 00:00'";
    $sql2 = "delete from spider_info where insertdate < '$date 00:00'";
    #$dbh->do($sql1);
    #$dbh->do($sql2);
    print "$sql1\n$sql2\n" if ($DEBUG);
};
