use strict;
use warnings;
use File::Basename qw(dirname);
use File::Path qw(make_path);

my ($out_root, $list_path) = @ARGV;
die "usage: $0 OUT_ROOT LIST_PATH\n" unless defined $out_root && defined $list_path;

my %added_lines_by_file;
my %has_link_candidate;
my $file;

while (my $line = <STDIN>) {
  chomp $line;

  if ($line =~ m{^\+\+\+ b/(.+)$}) {
    $file = $1;
    next;
  }

  next unless defined $file;
  next unless $line =~ /^\+(?!\+\+)(.*)$/;

  my $content = $1;
  push @{$added_lines_by_file{$file}}, $content;
  $has_link_candidate{$file} = 1 if $content =~ m{https?://}i || $content =~ /\bhref\s*=/i;
}

make_path($out_root);
open my $list_fh, ">", $list_path or die "cannot write $list_path: $!";

for my $file (sort keys %added_lines_by_file) {
  next unless $has_link_candidate{$file};
  next if $file =~ m{(?:^|/)\.\.(?:/|$)};

  my $out_path = "$out_root/$file";
  make_path(dirname($out_path));
  open my $out_fh, ">", $out_path or die "cannot write $out_path: $!";
  for my $line (@{$added_lines_by_file{$file}}) {
    print {$out_fh} "$line\n";
  }
  close $out_fh;
  print {$list_fh} "$out_path\n";
}

close $list_fh;
