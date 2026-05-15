use strict;
use warnings;
use File::Basename qw(dirname);
use File::Path qw(make_path);

my ($out_root, $list_path) = @ARGV;
die "usage: $0 OUT_ROOT LIST_PATH\n" unless defined $out_root && defined $list_path;

my $site_base_url = $ENV{DOCS_SITE_BASE_URL};
die "DOCS_SITE_BASE_URL is not set\n" unless defined $site_base_url && $site_base_url ne "";
$site_base_url =~ s{/+\z}{};

make_path($out_root);
open my $list_fh, ">", $list_path or die "cannot write $list_path: $!";

local $/ = "\0";
while (my $file = <STDIN>) {
  chomp $file;
  next if $file =~ m{(?:^|/)\.\.(?:/|$)};
  next unless -f $file;

  open my $in_fh, "<", $file or die "cannot read $file: $!";
  my %seen;
  while (my $line = <$in_fh>) {
    while ($line =~ /\bhref\s*=\s*(["'])(.*?)\1/gi) {
      my $href = $2;
      $href =~ s/^\s+|\s+$//g;
      next if $href eq "";
      next if $href =~ m{^https?://}i;
      next if $href =~ m{^(?:#|mailto:|tel:|javascript:|data:)}i;

      my $url;
      if ($href =~ m{^//}) {
        $url = "https:$href";
      } elsif ($href =~ m{^/}) {
        $url = "$site_base_url$href";
      } else {
        $url = "$site_base_url/$href";
      }
      $seen{$url} = 1;
    }
  }
  close $in_fh;

  next unless %seen;
  my $out_path = "$out_root/$file";
  make_path(dirname($out_path));
  open my $out_fh, ">", $out_path or die "cannot write $out_path: $!";
  for my $url (sort keys %seen) {
    print {$out_fh} "<$url>\n";
  }
  close $out_fh;
  print {$list_fh} "$out_path\n";
}
close $list_fh;
