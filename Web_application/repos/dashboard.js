$(document).ready(function(){

    //  cards 
//  assts card
let totalAssets = document.getElementById('totalAssets');
let availableAssets = document.getElementById('availableAssets');
let onMoveAssets = document.getElementById('onMoveAssets');
// tags card
let totalTags = document.getElementById('totalTags');
let avaiableTags = document.getElementById('availableTags');
let assignedTags = document.getElementById('assignedTags');

// readers card
let totalReaders = document.getElementById('totalReaders');
let onlineReaders = document.getElementById('onlineReaders');
let offlineReaders = document.getElementById('offlineReaders');

// charts

// movements chart
let movements = document.getElementById('movementsChart');

// alerts chart
let alerts = document.getElementById('alertsChart');

// table holder
let tableHolder = document.getElementById('tableHolder');

// tile holder
let tileHolder = document.getElementById('tileHolder');

// performance panel 
let performancePanel = document.getElementById('performancePanel');

// let opts 
// let chartTypeBtn = document.getElementById('');
setCards(totalAssets, availableAssets, onMoveAssets, totalTags, avaiableTags, assignedTags, totalReaders, onlineReaders, offlineReaders);
setChart(movements, 'bar', alerts, 'bar');
setTable(tableHolder);
setTiles(tileHolder);
setPerformancePanel(performancePanel);

setInterval(()=>{
    setCards(totalAssets, availableAssets, onMoveAssets, totalTags, avaiableTags, assignedTags, totalReaders, onlineReaders, offlineReaders);
}, 5000);
// setInterval(()=>{
//     setChart(movements, 'bar', alerts, 'bar');
// }, 10000);
setInterval(()=>{
    setTable(tableHolder);
}, 5000);
setInterval(()=>{
    setTiles(tileHolder);
}, 5000);
setInterval(()=>{
    setPerformancePanel(performancePanel);
}, 5000);
})

function setCards(el1, el2, el3, el4, el5, el6, el7, el8, el9){
    console.log(1);
    $.post(
        "http://127.0.0.1:3000/setCards",
        function(result){
            el1.innerText = result[0];
            el2.innerText = result[1];
            el3.innerText = result[2];

            el4.innerText = result[3];
            el5.innerText = result[4];
            el6.innerText = result[5];

            el7.innerText = result[6];
            el8.innerText = result[7];
            el9.innerText = result[8];
        }
    );
}
function setChart(movements , chartType1 = 'bar', alerts, chartType2 = 'bar'){
    console.log(2);
    // let chart1;
    // let chart2;

    // chart1.destory();
    // chart2.destory();
    let colors = '#3f9dec';
    let months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    $.post(
        "http://127.0.0.1:3000/getChartData",
        function(result){
            let config1 = {
                type : chartType1,
                data:{
                    labels : months,
                    datasets : [{
                        backgroundColor : colors,
                        data : result[0]
                    }]
                },
                options : {
                    maintainAspectRatio : false,
                    legend : {display : false},
                    title : {display : false}
                }
            }

            let config2 = {
                type : chartType2,
                data:{
                    labels : months,
                    datasets : [{
                        backgroundColor : colors,
                        data : result[1]
                    }]
                },
                options : {
                    maintainAspectRatio : false,
                    legend : {display : false},
                    title : {display : false}
                }
            }

            // chart1 = new Chart(movements, config1);
            // chart2 = new Chart(alerts, config2);
            new Chart(movements, config1);
            new Chart(alerts, config2);
        }
    );
}

function setTable(panel){
    console.log(3);
    $.post(
        "http://127.0.0.1:3000/setTable",
        function(result){
            let arr = ['serial no.','asset id','starting point','destination','date','time', 'custodian name','custodian id','requestor name','requestor id','request status'];
            let element =  document.querySelector('table');
            element.remove();
            let table = document.createElement('table');
            table.className = 'dynamicTable';
            let thead = document.createElement('thead');
            let tbody = document.createElement('tbody');
            let tr = document.createElement('tr');

            for(let i = 0; i<arr.length; i++){
                let th = document.createElement('th');
                th.innerText = arr[i];
                tr.appendChild(th);
            }
            thead.append(tr);

            for(let x in result){
                let row = tbody.insertRow(x);
                for(let i = 0; i < Object.values(result[x]).length; i++){
                    if( Object.values(result[x])[i] != null){
                    row.insertCell(i).innerText = Object.values(result[x])[i];
                    }
                    else{
                        row.insertCell(i).innerText = 'NA';  
                    }
                } 
            }
            table.append(thead);
            table.append(tbody);
            panel.append(table); 
        }
    )
}
function setTiles(panel){
    console.log(4);
    $.post(
        "http://127.0.0.1:3000/getTileData",
        function(result){
            let len = result[0].length;
            for(let i = 0; i < len; i++){
                let tile = document.createElement('section');
                tile.className = 'tile';
                let tileHeader = document.createElement('div');
                tileHeader.className = 'deptName';
                let tileData = document.createElement('div');
                tileData.className = 'deptAssets';

                tileHeader.innerText = result[0][i];
                tileData.innerText = result[1][i];

                tile.append(tileHeader, tileData);
                panel.append(tile);
            }
        }
    )
}

function setPerformancePanel(performancePanel){
    console.log(5);
    $.post(
        "http://127.0.0.1:3000/getPerformanceData",
        function(result){
            console.log(result);
            let len = result[0].length;
            for(let i = 0; i < len; i++){
                let tile = document.createElement('section');
                tile.className = 'ptile';
                let tileHeader = document.createElement('div');
                tileHeader.className = 'tileName';
                let tileData = document.createElement('div');
                tileData.className = 'tileValue';

                tileHeader.innerText = result[0][i];
                tileData.innerText = result[1][i];

                tile.append(tileHeader, tileData);
                performancePanel.append(tile);
            }
        }
    )
}