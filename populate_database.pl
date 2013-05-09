use warnings;
use strict;

die "need two inputs\n" unless (@ARGV == 2);
my $inputfile = $ARGV[0];
my $outputfile = $ARGV[1];
open (my $INPUT, "<", $inputfile);
open (my $OUTPUT , ">", $outputfile);
my $index = 0;
while(<$INPUT>) {
	chomp;
	my @fields = split;
	$index++;
	print $OUTPUT "p$index = Mouse.objects.create(name=\'$fields[0]:$fields[1]\',chrom=\'$fields[0]\',position=\'$fields[1]\',gene=\'$fields[2]\',strand=\'$fields[3]\',annot1=\'$fields[4]\',annot2=\'$fields[5]\',alu=\'$fields[6]\',repnonalu=\'$fields[7]\',ref=\'$fields[8]\')\n";
}
close $INPUT;
close $OUTPUT;
