# my @allq[4] = [0 xx 4];
# my @allt[4] = [0 xx 4];
# my @error[4] = [0 xx 4];
# my \n  = 40;
# my @p;
# for 0..0 {
#     push @p, start subsum($_, n / 1);    
# }

# await @p;
# say "{@allq.sum / n} {@allt.sum / n}";

# sub subsum(\i, \n) {
#     my ($q, $t);
#     for 1..n {
#         my $rel =  run <python gding19.py>, :out;
#         $rel = $rel.out.slurp(:close);
#          $rel !~~ /failed/ ?? (($q, $t) = ($rel ~~ /\s (\d+) \n (.*) \n $/)[0..1])
#                            !! @error[i]++ ;
#         @allq[i] += +$q;
#         @allt[i] += +$t;
#     }
# }
sub calcae( $c ) {
    my ($n,$a) = $c; 
    # say "$n $a";
    return 4.5 * sqrt(4*$a**2 + 12*$n*$a**4);
}

calcae($_).say for ((128,256,512,1024) Z (4.19 xx 4));
my \idx = 4;
my @e = [3000, 4500, 6200, 8800, 2100];
my @lll = [2255041, 9205761, 26038273, 28434433, 7557773];
my \q = @lll[idx];
my $D = 0;
for 1..4 -> \i {
    say q / (2**i);
}

say "q/2";
say q/2;
say q/4 - @e[idx];

# $D = 6500000 + @e[idx];
# say (q/2).round - ((q/4).Int - $D)/15,"< k <", (q/2).round + ((q/4).round - $D)/15;



say "q/4";
# say (q/4).Int/13;
say my \q_4 = (q/4).Int / 15;
$D = (^q_4).grep(* % 1000 == 0).max;
say $D;
say $D - @e[idx];
# $D = 142000 + @e[idx];
say (q/4).round - ((q/4).Int - $D)/14,"< k <", (q/4).round - $D;

# say "q/8";
# say q/8 / (15/2 + 1);
# $D = (^((q/8 / (15/2 + 1)).Int)).grep(* % 1000 == 0).max;
# say $D;
# say $D - @e[idx];
# say q/8 - (q/8 - $D)/15,"< k <", q/8 - $D/2;

say "q/16";
say q/16 / (11/4 + 1);
say my \q_16 = (4*(3*q/4+1).Int - 11*(q/4).round) / 15;
$D = (^q_16).grep(* % 1000 == 0).max;
say $D;
say $D - @e[idx];
# $D = 122000 + @e[idx];
# say q/16 + $D/4,"< k <", q/16 + (q/16 - $D)/11;
say ((q/4).round + $D) / 4 , "< k <", ((3*q/4 + 1).Int - $D) / 11;

say "q/32";
say my \q_32 = (q/4).round / 15;
$D = (^q_32).grep(* % 1000 == 0).max;
say $D;
say $D - @e[idx];
# $D = 122000 + @e[idx];
say ((q/4).round + $D) / 8 , "< k <", ((q/4).round - $D) / 7;



say "";
say q/2/16;
my $k = (^((q/2/16).Int)).grep(* % 1000 == 0).max;
say $k;
say $k = $k - @e[idx];
say q/4 - $k;
say q/4 + $k;



[3, -5, 4, 8, -6, 4, 6, 3, 5, 1, -1, 0, 3, 0, 0, -3, 7, -6, 4, -6, 0, -5, -4, 0, -2, 3, 5, -3, -3, -4, -10, 2, 1, 8, 2, -3, -2, -3, -4, -7, 3, -7, -1, -7, -6, 0, -6, 2, -2, 6, -4, 6, 1, -7, -4, 0, 1, 0, 4, 1, 3, 6, -2, 7, -1, 2, 4, -2, 3, 8, -1, -5, 1, -5, -1, 2, 5, -2, -2, -5, 0, -1, 1, -5, -4, 4, 0, -4, -5, 9, -1, 3, 3, 1, 5, 1, 1, 1, 6, -2, 4, 4, -4, -9, -1, -13, 4, -8, -1, 11, -2, 2, -5, 3, 2, 4, 0, 2, -1, -1, 2, -4, 1, 4, -1, 6, -1, -1, 1, -1, -1, -8, 9, 6, 6, 1, -3, -2, -2, -1, -2, -3, -8, -3, -3, 2, 4, 2, 3, 4, -1, -3, -2, 0, 4, -4, -1, 2, 4, 4, -4, -1, 6, 1, -3, -3, 0, -3, 6, -3, -3, 0, 1, 5, -1, 1, 0, -6, 1, -2, -6, -1, -6, -6, 1, -1, 3, 0, -1, 4, 6, -1, -6, 6, 8, 6, 2, 1, -9, -2, 2, -2, -4, -3, -1, -1, -1, -3, 1, 2, -2, -4, 2, -1, -3, -4, 4, -1, 9, 1, 8, -2, 5, -3, 4, 0, -3, -5, 3, 2, 3, -10, -5, 2, -7, 1, 1, 2, 4, 5, 9, -4, 8, 4, 6, 7, 0, -7, 5, -9, -5, 3, 1, 2, 1, 1, -3, -7, 2, 4, 1, -1, -1, -9, -3, 2, 3, 3, 2, -4, -2, 4, -2, 2, 7, 0, 0, -3, -3, -7, -5, -2, -3, -2, -4, 0, -2, -9, 1, 14, -4, 1, -1, 1, -5, 2, 1, -3, -6, 0, -3, -1, -2, 11, 0, -6, 2, -1, -1, 11, -7, 5, -2, 0, -9, -2, -1, 6, -6, 4, 5, 1, -3, -3, 5, -1, 2, -2, 7, -4, 2, -1, -5, -2, -5, 7, 1, -6, 4, 2, -6, -4, 3, -1, -5, -4, -2, 5, -7, 1, 4, 4, -4, -2, -8, -5, -2, 7, 7, -1, -10, 6, 2, 6, -5, 2, 0, -3, 1, 4, 9, -4, 2, 4, 3, 7, -4, 9, 4, 5, 6, 0, 5, 0, -2, 0, -3, 0, 2, -5, 3, 7, 0, -5, 5, 3, 4, 3, 8, 3, 14, 0, -2, 3, -4, 7, 4, -1, -2, -7, 4, -7, -4, 3, 2, -1, -1, 4, 2, -3, -4, -7, -6, 9, -3, -8, 2, 0, -9, 3, 4, 5, 7, 2, -1, -8, 1, -3, -1, 3, -1, -4, 4, 8, 6, 1, 1, 5, -7, 0, -4, -2, 7, -8, 3, 1, 2, 2, 4, -5, 2, -4, 6, 4, 0, -1, 1, -2, 2, 7, 0, 0, -2, -9, -1, -1, -8, -2, 3, -7, -2, 1, -4, 11, 2, 4, -1, 1, -3, -3, -8, -5, 0, 5, 0, -12, 1, -4, 2, -4, 5, -5, -1, 0, -8, 0, -4, -1, -3, 0, -8, 3]