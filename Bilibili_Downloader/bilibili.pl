#!/usr/bin/env perl
use LWP::Simple;
use LWP::UserAgent;
use utf8;
use JSON;
use strict;
use Data::Dumper;
use File::Basename;
use File::Basename;
use HTTP::Message;

binmode(STDIN,':encoding(utf8)');
binmode(STDOUT,':encoding(utf8)');

if ( $ARGV[0] ){

    my $quality = 3;
    if ( $ARGV[1] ){
		$quality = ord($ARGV[1]);
		$quality > 3 ? $quality = 3 : $quality < 0 ? $quality = 1 : $quality;
    }else{
        print " Not selected video quality.\n  download high quality video for default.\n";
    }
    #视频清晰度
    
    my $getCid = "http://api.bilibili.cn/view?check_area=1&batch=1&type=json&appkey=0a99fa1d87fdd38c&platform=ios&id=";
    $getCid = $getCid.$ARGV[0];
    print " Getting cid for ",$ARGV[0],"\n";
    #构建获取CID的URL

    my $requestCID = HTTP::Request->new('GET' => $getCid);
    my $ua = new LWP::UserAgent;
    $ua->agent("Safari");
    my @header = ("Accept" => "*/*","Accept-Language" => "en-us","Connection"=>"Keep-Alive");
    $requestCID->header(@header);
    my $res = $ua->request($requestCID);
    my $jsonString = $res->content();
    #向B站索要av号所对应的CID

    if ($jsonString) {
        my $cidJSON = from_json($jsonString);
        #获取CID
        
        my $download = "http://interface.bilibili.cn/playurl?otype=json&quality=3&appkey=0a99fa1d87fdd38c&platform=ios&cid=";
        $download .= ${${$cidJSON}{list}}{0}->{cid};
        print " Getting download link for\n\033[32m   ",$cidJSON->{"title"},"\n     \033[0m\033[37m",$cidJSON->{"description"},"\033[0m\n";
        #获取下载链接
		
        my $requestDownloadURL = HTTP::Request->new('GET' => $download);
        $requestDownloadURL->header(@header);
        $res = $ua->request($requestDownloadURL);
        my $playurlString = $res->content();
        if ($playurlString){
            my $playJSON = from_json($playurlString);
			
            if($playJSON->{result} eq "suee"){
            	my @downloadURLs = ();
            	my @durl = $playJSON->{durl};
            	my $root = \@durl;
            	my $i = 0;
            	my $count = $#{$root->[0]}+1;
            	for(;$i<$count;$i++){
               		push @downloadURLs,$root->[0]->[$i]->{'url'};
            	}
            	print " Success! ",$#downloadURLs + 1," files to download.\n";
				my $count = 1;
				mkdir ${${$cidJSON}{list}}{0}->{cid};
				foreach my $link (@downloadURLs) {
					print " Downloading No.$count file...";
					if (-e "${${$cidJSON}{list}}{0}->{cid}/$count.mp4") {
						print "\n   \033[0m\033[37mExists ${${$cidJSON}{list}}{0}->{cid}/$count.mp4. Skip!\n\033[0m";
						$count++;
						next;
					}
					getstore($link,"${${$cidJSON}{list}}{0}->{cid}/$count.mp4") or print "\n Cannot download No.$count file x_x"; 
					$count++;
					print "\n";
				}
				
				my $danmaURL = "http://comment.bilibili.cn/${${$cidJSON}{list}}{0}->{cid}.xml";
				print " Downloading danma file...";
				if (-e "${${$cidJSON}{list}}{0}->{cid}/${${$cidJSON}{list}}{0}->{cid}.xml") {
					print "\n   \033[0m\033[37mExists danma file. Skip!\033[0m";
				} else {
					my $can_accept = HTTP::Message::decodable;
					my $requestForDanma = HTTP::Request->new('GET' => $danmaURL);
					my $ua = new LWP::UserAgent;
					$ua->agent("Safari");
					my @headerForDanma = ("Accept-Encoding" => $can_accept,"Accept-Language" => "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3","Accept" => "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Connection"=>"Keep-alive");
					$requestForDanma->header(@headerForDanma);
					my $res1 = $ua->request($requestForDanma);
					my $danmaData = $res1->decoded_content;
					Encode::_utf8_off($danmaData);
					open my $fh,'>:utf8',"${${$cidJSON}{list}}{0}->{cid}/${${$cidJSON}{list}}{0}->{cid}.xml";
					binmode $fh;
					print $fh $danmaData;
				}
				print "\n";
				my $dir = dirname($0);
				system "$dir/danmaku2ass.py -o ${${$cidJSON}{list}}{0}->{cid}/video.ass -s 1280x720 ${${$cidJSON}{list}}{0}->{cid}/${${$cidJSON}{list}}{0}->{cid}.xml";
				system "rm ${${$cidJSON}{list}}{0}->{cid}/${${$cidJSON}{list}}{0}->{cid}.xml";
				if ($count > 2) {
					print " $cidJSON->{title} has more than one video. You should combine them.\n";
				}
				print " All done!\n";
            }else{
                print " Fail to get download URL.\n";
            }
        }
    }
}else{
    print "Please input av id.\n";
}
