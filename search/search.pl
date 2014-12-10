#!/usr/bin/perl

use vars qw/$libpath/;
use FindBin qw($Bin);
BEGIN { $libpath="$Bin" };
use lib "$libpath";
use lib "$libpath/../lib";

open(file, "$Bin/search.tmpl");
@html = <file>;
close(file);

use DBI;
use CGI;
print "Content-type: text/html\n\n";

$| = 1;

my %dbconfig = loadconfig("$Bin/conf/db.config");
my ($dbname, $dbhost, $dblogin, $dbpassword) = ($dbconfig{dbname}, $dbconfig{dbhost}, $dbconfig{dblogin}, $dbconfig{dbpassword});
my $dbh = DBI->connect("dbi:mysql:dbname=$dbname;host=$dbhost",$dblogin,$dbpassword,{AutoCommit=>1,RaiseError=>1,PrintError=>0});

use Sphinx::Search;
my $q = new CGI;

$url = $q->param('url');
$api = $q->param('api');
$param = $q->param('param');
$query = $q->param('query');
$page = $q->param('page');
$limit = $q->param('limit');
$blocktitle = $q->param('blocktitle');
showhtml($query, @html) unless ($api);

unless ($query)
{
    $query = $input{query} || $ARGV[0];
}
print "$query\n";

my $sphinx = Sphinx::Search->new();     # Вызываем конструктор
$sphinx->SetServer( '127.0.0.1', 9312); #localhost', 3312 );
$limit = 10 if ($api && !$limit);
$limit = 2000 unless ($limit);
$offset = 0;

if ($page)
{
    $offset = (($page - 1) * $limit);
}
$sphinx->SetLimits($offset, $limit);

#$sphinx->SetLimits($offset, $limit);
print "$sphinx\n" if ($DEBUG);
print 'Connected... '.$sphinx->_Connect() if ($DEBUG);

my $text = $query;

if ($text)
{
   search($text);
}

sub search
{
    my ($item, $DEBUG) = @_;

    print "Searching for $item...\n";

    $index = "travel";
    if ($item)
    {
       %weights=(name=>3, annotation=>1);
       #$results = $sphinx->SetMatchMode(SPH_MATCH_ANY)     # Режим поиска совпадений
	$results = $sphinx->SetMatchMode(SPH_MATCH_EXTENDED)
                      ->SetSortMode(SPH_SORT_RELEVANCE) # Режим сортировки
                      ->SetFieldWeights(\%weights)      # Вес полей
                      ->Query($item, $index);      # Поисковый запрос

       $found=$results->{total_found};
       $attrs=$results->{words};
       my $err = $sphinx->GetLastError;
    };

    my $i;
    if ($found && !$api)
    {
	$pages = int(($found / $limit) + 1);
	print "<p>Found <b>$found</b> scans from Digital Repository </p>\n";
	showpages($pages);
    }

    for (my $x=0; $x<$found; $x++)
    {
        $url = $results->{matches}->[$x]->{url};
	$doc = $results->{matches}->[$x]->{id};
	%info = %{$results->{matches}->[$x]};
	#print "<hr />\n";
	my ($title, $post, $url) = ($info{title}, $info{post}, $info{url});
	foreach $item (sort keys %info)
	{
	   # print "$item $info{$item} <br />\n";
	}

print <<"EOF";
<blockquote>
<a href=\"$url\">$title</a>
<br>
$post
</blockquote>
EOF

	$i++;
	$rating{$doc} = $i;

        if ($doc)
        {
            print "$x id => $doc\n" if ($DEBUG);
            $ids.="$doc, ";
        };

    }

    print "$ids<br />\n";

    my $show = 0;
    if ($ids && $show)
    {
        $ids=~s/\,\s+$//g;
        $sqlquery = "select id, title, post, url from posts where id in ($ids)";
        print "$sqlquery\n" if ($DEBUG);
        my $sth = $dbh->prepare("$sqlquery");
        $sth->execute();

        while (my ($id, $title, $post, $url, $token, $type, $amount) = $sth->fetchrow_array())
        {
	     print "$title<br />\n";
             $class{$token} = "$token/$type";
	     $tokens{$token} = $id;
	     $result{$id} = $url;
        }
    }

    my $id;

    foreach $i (sort {$rating{$a} <=> $rating{$b}} keys %rating)
    {
	$id++;
	my $url = $result{$i};
	my $level2 = $url;
	$level2=~s/level3/level2/g;
	#$level2="/digital/?q=node/$i";

	unless ($api)
	{
	    if ($level2)
	    {
	        print "<a href=\"$level2\" title=\"$i\"><img src=\"$result{$i}\"></a>\n ";
	    };
	};

    }

    showpages($pages, "<br /><br />") unless ($api);
}

sub showpages
{
    my ($pages, $html, $DEBUG) = @_;

    print "$html<p>Pages:&nbsp;";
    $pages = 50 if ($pages > 50);
    $page = 1 unless ($page);
    for ($i=1; $i<=$pages; $i++)
    {
	unless ($i eq $page)
	{
	print "<a href=/cgi-bin/search.cgi?query=$query&page=$i>$i</a>&nbsp;";
	}
	else
	{
	    print "<b>$i</b>&nbsp;";
	}
    }
    print "</p>";
}

sub finder
{
    my ($dbh, $content, $DEBUG) = @_;
    my $output;

    my @words = split(/\s+/, $content);

    my $sqlwords;
    for ($i=0; $i<=$#words; $i++)
    {
	$word = $words[$i];
	$word=~s/[\,\.\?\!]//g;
	$tokens{$word} = $i;

	if ($word=~/[A-Z]/)
	{
	    $wordtoken = $dbh->quote($word);
	    $sqlwords.="$wordtoken, ";
	};
    }

    if ($sqlwords)
    {
	$sqlwords=~s/\,\s+$//g;
	$sqlquery = "select entity, type, amount from names where entity in ($sqlwords)";
	print "$sqlquery\n"; # if ($DEBUG);
        my $sth = $dbh->prepare("$sqlquery");
        $sth->execute();

        while (my ($token, $type, $amount) = $sth->fetchrow_array())
        {
	     #$output.="$token/$type ";
	     $class{$token} = "$token/$type";
	}
    }

    for ($i=0; $i<=$#words; $i++)
    {
        $word = $words[$i];
	$tmpword = $word;
	$tmpword=~s/[\,\.\?\!]//g;
	my $wordout = $class{$tmpword} || "$word/O";
	$output.="$wordout ";  
    }

    $output=~s/^\s+|\s+$//g;
    print "$output\n";

    return;
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

# select * from authorities where entity like '%Schmier%' limit 10;

sub showhtml
{
    my ($query, @html) = @_;

    foreach $item (@html)
    {
	$item=~s/\%\%query\%\%/$query/gi;
	print "$item\n";
    }
}

sub showsearchform
{
print <<"EOF";
<center>
<p>
<form action="/cgi-bin/search.cgi" method=get>
Search: <input type="text" name="query" value="$query" /><br />
<input type="submit" value="Find Scans!">
</form>
</p>
</center>
EOF

}

