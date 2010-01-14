#! /usr/bin/env perl
use strict;

#
# addCit2owl.pl
# David Landan
# July 5, 2008
# 
# use: ./addCit2owl.pl goldfile.owl bibfile.bib
#
# given the current gold-xxxx.owl file, make sure that all refernces within
# comment fields have corresponding citation tags.  print warning if a
# reference is found in the .owl that isn't in the goldrefsfile.
#

if ($#ARGV != 1) {
  print "use: ./addCit2owl.pl goldfile.owl bibfile.bib\n";
  die "requires exactly two arguments.\n";
}

my $owlfile = $ARGV[0];
my $tmpfile = $owlfile . ".tmp";
my $bibfile = $ARGV[1];

# First, make a hash whose keys are the RefIDs in the bibfile.

my %bibkeys = ();

if (!open BIBFILE, "<$bibfile") {
  die "couldn't read from $bibfile.\n";
}

while (<BIBFILE>) {
  chomp;
    if (/\@/) {
    s/,//;
    my @line = split(/\{/);
    my $ref = $line[1];
    $bibkeys{$ref}++;
  }
}

close (BIBFILE);

# Next, read owlfile, print lines to tmpfile.  Add citations where they
# don't already exist, unless they're not in the bibkeys hash.  For those
# not in bibkeys, print a warning message to STDOUT.

if (!open OWLFILE, "<$owlfile") {
  die "couldn't read from $bibfile.\n";
}

if (!open TMPFILE, ">$tmpfile") {
  die "couldn't write to $tmpfile.\n";
}

my %refs = ();
my $inCommentFlag = 0;
my $inBlock = 0;
my @block = ();
my %blockCitations = ();

my $lineNo = 0;

#added my Scott Farrar
my @missing = ();

while (<OWLFILE>) {
  chomp;
  $lineNo++;
  # keep track of each block at the level of ObjectProperty or Class,
  # since this is where comment blocks go.  we do this to track whether
  # citations we're about to write already exist within this block
  if ((/\<owl:ObjectProperty/) || (/\<owl:Class/) || (/\<owl:DataProperty/)) {
    unless (/\/\>/) {
      $inBlock = 1;
    }
  }
  # if we're in one of the blocks mentioned above, keep track of comments,
  # refs, and existing citations.
  if ($inBlock == 1) {
    push @block, $_;
    if (/\<rdfs:comment/) {
      $inCommentFlag = 1;
    }
    if ($inCommentFlag == 1) {
      if (/\[/) {
        getRefs($_);
      }
    }
    if (/\\rdfs:comment/) {
      $inCommentFlag = 0;
    }
    # refs are set, now we check to see which ones are already taken care of
    if (/\<biblio:hasEntry/) {
      my @foo = split(/\"/);
      $foo[1] =~ s/\&biblio;//;
      $blockCitations{$foo[1]}++;
    }
    # if we're at the end of the block, get ready to print
    if ((/\<\/owl:ObjectProperty/) || (/\<\/owl:Class/) || (/\<\/owl:DataProperty/)) {
      $inBlock = 0;
      for (my $i=0; $i<$#block; $i++) {
	print TMPFILE "$block[$i]\n";
      }
      for my $ref (keys %refs) {
	unless (exists $blockCitations{$ref}) {
	  if (!exists $bibkeys{$ref}) {
	    print STDOUT "Warning: $ref not found in $bibfile.\n";
            push(@missing, $ref);
	  }
            my @pages = keys %{$refs{$ref}};
	    pop @pages;
	    print TMPFILE "\t<biblio:hasCitation>\n";
	    print TMPFILE "\t    <biblio:Citation rdf:about=\"\&gold;$ref\_$lineNo\">\n";
	    print TMPFILE "\t\t<biblio:hasEntry rdf:resource=\"\&goldbib;$ref\"/>\n";
	    if (scalar(@pages) > 0) {
	      my $pages = join(', ',(sort {$a <=> $b} @pages));
	      print TMPFILE "\t\t<biblio:hasPageInformation>$pages</biblio:hasPageInformation>\n";
	    }
	    print TMPFILE "\t    </biblio:Citation>\n";
	    print TMPFILE "\t</biblio:hasCitation>\n";
	}
      }
      print TMPFILE "$_\n";
      # clean up and prepare for the next block
      %refs = ();
      @block = ();
      %blockCitations = ();
    }
  }
  # if we're not in a block that might contain a comment, just print the line
  else {
    print TMPFILE "$_\n";
  }
}

print STDOUT @missing;

close (INFILE);
close (TMPFILE);

# finally move the tempfile into the old .owl file's place

`mv $tmpfile $owlfile`;


# getRefs function
#    take a line that contains square brackets, break it down to get an
#    array of stuff between brackets.  then, take each ref (separated by
#    semicolons) and send it to the normalize function.  now it's ready to
#    be added to the hash (or incremented if it already exists).

sub getRefs {
  my @line = split(/\[/, $_);
  my @temp = ();
  for my $section (@line) {
    if ($section =~ /\]/) {
      my @foo = split(/\]/, $section);
      push @temp, $foo[0];
    }
  }
  for my $refgroup (@temp) {
    my @foo = split('; ', $refgroup);
    for (my $i=0; $i<=$#foo; $i++) {
      my @refPage = split(/[,:]/, $foo[$i]);
      my $ref = $refPage[0];
      my @pages = ();
      for (my $j=1; $j<=$#refPage; $j++) {
        if ($refPage[$j] =~ /citing/) {
          $refPage[$j] = '';
        }
        if (($refPage[$j] =~ /[A-Z]/) || ($refPage[$j] =~ /19\d{2}/) || ($refPage[$j] =~ /20\d{2}/)) {
          $ref .= $refPage[$j];
        }
        else {
          $refPage[$j] =~ s/\s+//g;
          push @pages, $refPage[$j];
        }
      }
      my $ref = normalize($ref);
      if (($ref =~ /[A-Z]/) && (($ref =~ /19\d{2}/) || ($ref =~ /20\d{2}/))) {
        $refs{$ref}{-1}++;
        for my $pg (@pages) {
          $refs{$ref}{$pg}++;
        }
      }
    }
  }
}

# normalize function
#    take a citation, and return the form defined by Farrar
#    other regex may be needed...

sub normalize {
  my $ref = @_[0];
  $ref =~ s/_et/-et/;
  $ref =~ s/et al\./-etal/;
  $ref =~ s/[A-Z]\.//g;
  $ref =~ s/ and //;
  $ref =~ s/,//g;
  $ref =~ s/ //g;
  return $ref;
}

