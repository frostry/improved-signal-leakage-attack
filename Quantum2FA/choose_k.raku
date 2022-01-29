my \m0 = slurp 'm0';
my \m1 = slurp 'm1';
# say m0;
my @res_0 = $/[0].flat if m0 ~~ /[(.+?) \n\n]+/; 
my @res_1 = $/[0].flat if m1 ~~ /[(.+?) \n\n]+/;
@res_0 = @res_0.map(*.Str);
@res_1 = @res_1.map(*.Str);
# say @res_0.elems;
# say @res_0 == @res_1;

my %signal = 0 => 0, 0.12499 => 1, 0.24998 => 2, 0.374969 => 3, 0.500041 => 4, 0.625031 => 5, 0.75002 => 6, 0.87501 => 7;
my %all;
for 0..@res_0.end -> \i {
    if @res_0[i] ~~ /bhat\: . (\d+) / {
        my $k = $/[0].Int;
        say $k;
        my @m0 = @($/[0]).map(*.Rat) if @res_0[i] ~~ /[(\d\.\d+) \s]+/;
        my @m1 = @($/[0]).map(*.Rat) if @res_1[i] ~~ /[(\d\.\d+) \s]+/;
#         say @m0;
#         say @m1;
        my %k = Empty;
#         say [-8..8].Str;
        for -8..8 -> $i {
            %k{$i} = [@m0[$i + 8], @m1[$i + 8]];
#             print "({%signal{@m0[$i + 8]}, %signal{@m1[$i + 8]}}) ";
        }
        
        print "    " ~ $_ for (-8..0).reverse;
        print "\n ";
        for (@m0[0..8] Z @m1[0..8]).reverse {
            print "({%signal{$_[0]}} {%signal{$_[1]}}) "
        }
        print "\n     ";
        print "     " ~ $_ for 1..8;
        print "\n       ";
        for @m0[9..@m0.end] Z @m1[9..@m1.end] {
            print "({%signal{$_[0]}} {%signal{$_[1]}}) "
        }
        print "\n";
#         %all{$k} = %k;
    }
}
