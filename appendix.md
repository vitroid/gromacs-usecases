### 9-1 VPN接続

岡山大学理論化学研究室所有の計算サーバ(Xeon 96 core, IP `192.168.3.220`)にリモートアクセスします。設定情報は別途お渡しします。

うまく接続できない場合は、Amazon EC2を利用します。

#### 9-1-1 Macの場合

System Settings->VPN->Add VPN Configurationで、設定を入力します。

https://www.cc.uec.ac.jp/ug/ja/remote/vpn/l2tp/macos114/index.html
が参考になります(入力する内容は適宜おきかえて下さい)

#### 9-1-2 Windowsの場合

https://www.seil.jp/saw-mpc/doc/sa/pppac/use/pppac-client/win11_l2tp.html
が参考になります(入力する内容は適宜おきかえて下さい)

コントロールパネル→ネットワークと共有センター→アダプタの設定変更→VPNを選ぶ→プロパティ→セキュリティ→次のプロトコルを許可する→CHAPにチェック!!! (ふう。なんでこんなに深いの)

### 9-2 Amazon EC2の個人利用

Amazon EC2の無料枠でも、そこそこの計算はできます。

1. AWSにアカウントを作ります。クレジットカード番号が必要になります。
2. EC2ダッシュボードで、EC2インスタンスを作成します。インスタンスタイプt2.micro (2 cores)までなら、無料で利用できます。
3. OSにはUbuntuを選びます。(計算プラットホームとして利用するのに適しています)
4. そのほか、ほとんどの設定はデフォルトのままでいいですが、不明な点は講師にお尋ね下さい。
### 9-3 Gromacsとその他のツールのインストール

クラウドを使わなくても、Unix系のOSになら、GromacsやGenIceを簡単にインストールできます。


#### 9-3-1 Ubuntu/Debian Linuxの場合

(管理者権限で実行する必要があります。)
```shell
apt update
apt install gromacs python3 python3-pip
pip install numpy
pip install genice2
```

#### 9-3-2 Redhat/Amazon Linux/CentOS7の場合

EC2のAmazon Linux/RedHat Linuxではgromacsパッケージが見付かりませんでした。[RPM](https://rpmfind.net/linux/rpm2html/search.php?query=gromacs)から必要なものを個別にインストールする必要があるようです。

#### 9-3-3 MacOSの場合

Homebrewをセットアップしておきましょう。

HomeBrewでは、管理者権限なしにインストールできます。
```shell
brew install gromacs python3
pip install genice2
```

#### 9-3-4 Windowsの場合

(情報求む!)