// mapオブジェクトを取得:
const map = L.map('map');
const dataId = "std";
// 地図タイルレイヤーを作成:
const layer = L.tileLayer(`https://cyberjapandata.gsi.go.jp/xyz/${dataId}/{z}/{x}/{y}.png`, {
attribution: "<a href='https://maps.gsi.go.jp/development/ichiran.html' target='_blank'>地理院タイル</a>"
});
// 地図タイルレイヤーをマップへ追加:
layer.addTo(map);
//地図の中心()
map.setView([34.661826992540405, 133.92672479152682], 14);


const marks = [];
for(i=0;i<device_obj.length;i++){
  marks[i] = L.marker([device_obj[i][3], device_obj[i][2]]);
  marks[i].addTo(map);
  // マーカーに吹き出しを設定:
  marks[i].bindPopup('<a href=./'+device_obj[i][0]+'>'+device_obj[i][1]+'の気象情報へ</a>');
  // 吹き出しをポップアップ:
  marks[i].openPopup();
}
// //マーカーを設置
// marks[0] = L.marker([34.66286389017133, 133.99354934692386]);
// marks[0].addTo(map);
// // マーカーに吹き出しを設定:
// marks[0].bindPopup('<a href=./'+device_obj[0][0]+'>'+device_obj[0][1]+'の気象情報へ</a>');
// // 吹き出しをポップアップ:
// marks[0].openPopup();
