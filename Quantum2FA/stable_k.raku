my \q = 12289;
my @edge =  [768.0625, 2304.1875, 3840.3125, 5376.4375, 6912.5625, 8448.6875, 9984.8125, 11520.9375];
loop (my $i = 0; $i < q; $i += 10) {
    my $flag = True;
    for 1..8 -> $j {
        for @edge {
            $flag = False if abs($_ - $j * $i) < 8.5;
            $flag = False if abs($_ - (-$j * $i + q)) < 8.5;
        }
    }
    say $i if $flag;
}
