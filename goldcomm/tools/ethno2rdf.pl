#! /usr/bin/env perl
use strict;
use Encode;

#
# ethno2rdf.pl
#
# David Landan
# July 12, 2008
# 
# written for Scott Farrar & the GOLD Community project
#
# Takes the files LanguageCodes.tab and LanguageIndex.tab and produces
# UTF-8 formatted output RDF file called ethnologue15.rdf in the working
# directory.
#
# usage: ./ethno2rdf.pl [path/]LanguageCodes.tab [path/]LanguageIndex.tab
#

if ($#ARGV != 1) {
  die "usage: ./ethno2rdf.pl [path/]LanguageCodes.tab [path/]LanguageIndex.tab\n";
}

(my $codeFile, my $indexFile) = @ARGV;

my %lid2status = ();
my %lid2name = ();
my %lid2dials = ();
my %lid2pejors = ();
my %lid2alts = ();
my %lid2cids = ();
my %dial2cids = ();

# first we set things up by processing the LanguageCodes.tab file
# LanguageIDs map one:one with status & primary name.  They map one:many
# with CountryIDs, but we'll just get the first one in this file

if (!open(CODEFILE, "<:encoding(iso-8859-15)", "$codeFile")) {
  die "couldn't read from $codeFile\n";
}

while (<CODEFILE>) {
  chomp;
  $_ =~ s/\s+$//;
  unless ($_ =~ /^LangID/) {
    (my $lid, my $cid, my $status, my $name) = split(/\t/);
    $name = normalize($name);
    $lid2status{$lid} = $status;
    $lid2name{$lid} = $name;
    $lid2cids{$lid}{$cid}++;
  }
}

close (CODEFILE);

# next we get name variants (alternates & pejoratives), dialects, and
# the rest of the CountryIDs. 

if (!open(INDEXFILE, "<:encoding(iso-8859-15)", "$indexFile")) {
  die "couldn't read from $indexFile\n";
}

while (<INDEXFILE>) {
  chomp;
  $_ =~ s/\s+$//;
  unless ($_ =~ /^LangID/) {
    (my $lid, my $cid, my $type, my $name) = split(/\t/);
    $name = normalize($name);
    unless ($type =~ /D/) {
      $lid2cids{$lid}{$cid}++;
    }
    if ($type eq 'LA') {
      $lid2alts{$lid}{$name}++;
    }
    if ($type eq 'LP') {
      $lid2pejors{$lid}{$name}++;
    }
    if ($type eq 'D') {
      $lid2dials{$lid}{$name}++;
      $dial2cids{$name}{$cid}++;
    }
  }
}

close (INDEXFILE);

# now we're ready to write to the output file.

if (!open(OUTFILE, ">:encoding(UTF-8)", "ethnologue15.rdf")) {
  die "couldn't write to ethnologue15.rdf\n";
}

# header info first
print OUTFILE "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
print OUTFILE "<!DOCTYPE Ontology [\n";
print OUTFILE "<!ENTITY xsd \"http://www.w3.org/2001/XMLSchema#\" >\n";
print OUTFILE "<!ENTITY rdfs \"http://www.w3.org/2000/01/rdf-schema#\" >\n";
print OUTFILE "<!ENTITY gold \"http://www.linguistics-ontology.org/gold/\" >\n";
print OUTFILE "<!ENTITY rdf \"http://www.w3.org/1999/02/22-rdf-syntax-ns#\" >\n";
print OUTFILE "<!ENTITY countries \"http://www.geonames.org/countries#\">\n";
print OUTFILE "]>";
print OUTFILE "<rdf:RDF\n";
print OUTFILE "\txml:base=\"http://www.linguistics-ontology.org/data/languages/ethnologue15.rdf\"\n";
print OUTFILE "\txmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"\n";
print OUTFILE "\txmlns:rdfs=\"http://www.w3.org/2000/01/rdf-schema#\"\n";
print OUTFILE "\txmlns:gold=\"http://www.linguistics-ontology.org/gold/\">\n\n";
print OUTFILE "\t <rdf:Description rdf:about=\"\">\n\t\t<rdfs:comment>This material generated from the code tables downloaded from www.ethnologue.com, the online version of Gordon, Raymond G., Jr. (ed.), 2005. Ethnologue: Languages of the World, Fifteenth edition. Dallas, Tex.: SIL International. </rdfs:comment>\n\t</rdf:Description>\n";

# now language info for each LanguageID
for my $lid (sort keys %lid2status) {
  my $idx = 1;
  my $variety = getVariety($lid);
  my @cids = keys %{$lid2cids{$lid}};
  my @pejors = keys %{$lid2pejors{$lid}};
  my @alts = keys %{$lid2alts{$lid}};
  my @dials = keys %{$lid2dials{$lid}};
  print OUTFILE "\t<rdf:Description rdf:about=\"\&gold\;$lid\">\n";
  print OUTFILE "\t\t<rdf:type rdf:resource=\"\&gold\;AttestedVariety\"/>\n";
  print OUTFILE "\t\t<rdf:type rdf:resource=\"\&gold\;$variety\" />\n";
  print OUTFILE "\t\t<gold:hasISO639-3>$lid</gold:hasISO639-3>\n";
  for my $cid (@cids) {
    print OUTFILE "\t\t<gold:spokenIn rdf:resource=\"\&countries\;$cid\"/>\n";
  }
  print OUTFILE "\t\t<gold:name>$lid2name{$lid}</gold:name>\n";
  for my $name (@alts) {
    print OUTFILE "\t\t<gold:name>$name</gold:name>\n";
  }
  for my $name (@pejors) {
    print OUTFILE "\t\t<gold:pejorativeName>$name</gold:pejorativeName>\n";
  }
  print OUTFILE "\t\t<rdfs:comment> This material generated from the code tables downloaded from www.ethnologue.com, the online version of Gordon, Raymond G., Jr. (ed.), 2005. Ethnologue: Languages of the World, Fifteenth edition. Dallas, Tex.: SIL International. </rdfs:comment>\n";
  print OUTFILE "\t</rdf:Description>\n\n";
  
  
  for my $name (@dials) {
    my @cids = keys %{$dial2cids{$name}};
    print OUTFILE "\t<rdf:Description rdf:about=\"\&gold\;$lid";
    print OUTFILE $idx++ . "\">\n";
    print OUTFILE "\t\t<rdf:type rdf:resource=\"\&gold\;AttestedVariety\"/>\n";
    for my $cid (@cids) {
      print OUTFILE "\t\t<gold:spokenIn rdf:resource=\"\&countries\;$cid\" />\n";
    }
    print OUTFILE "\t\t<gold:name>$name</gold:name>\n";
    print OUTFILE "\t\t<rdfs:comment> This material generated from the code tables downloaded from www.ethnologue.com, the online version of Gordon, Raymond G., Jr. (ed.), 2005. Ethnologue: Languages of the World, Fifteenth edition. Dallas, Tex.: SIL International. </rdfs:comment>\n";
    print OUTFILE "\t</rdf:Description>\n\n";
  }
}
print OUTFILE "</rdf:RDF>\n";

# given a code for the language variety, return the variety
# print a warning to STDOUT and return UnknownVariety if its not
# one of: L, N, E, S
sub getVariety {
  my $lid = @_[0];
  my $result = "UnknownVariety";
  my $st = $lid2status{$lid};
  if ($st eq 'L') {
     $result = "LivingVariety";
  }
  elsif ($st eq 'N') {
    $result = "NearlyExtinctVariety";
  }
  elsif ($st eq 'E') {
    $result = "ExtinctVariety";
  }
  elsif ($st eq 'S') {
    $result = "SecondLanguageOnlyVariety";
  }
  else {
    print OUTFILE "UnknownVariety";
  }
  return $result;
}

# take a comma separated name, split it, and return a single string
# that has what came after the comma first.  this is equivalent to
# converting a name from "last, first [middle]" to "first [middle] last"
# if there's no comma, just return the string as it came in.
sub normalize {
  my $str = @_[0];
  my $result = $str;
  if ($str =~ /,/) {
    my @foo = split(/,\s+/, $str);
    $result = join(' ', reverse(@foo)); 
  }
  return $result;
}
