#!/usr/bin/perl

use LWP::Simple;

sub download
{
    my (@urls) = @_;
    foreach $url (@urls)
    {
	$id++;
	$filename = "./data/$id.html";
	unless (-e $filename)
	{ 
	    $wget = `wget -q \"$url\" -O $filename`;
	}
	$ids{$url} = $id;
    }
}

while (<>)
{
    my $str = $_;
    $str=~s/\r|\n//g;
    my @ritems = split(/\|/, $str);
    @items = reverse @ritems;

    $url = $items[1];
    $url=~s/^\"|\"$//g;
    unless ($url=~/http/)
    {
	$url = "http://$url" if ($url);
    }

    if ($url)
    {
	push(@urls, $url);
    }
}

download(@urls);
