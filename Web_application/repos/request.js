let mTotalRequests = document.getElementById('mTotalRequests');
let mPendingRequests = document.getElementById('mPendingRequests');
let mApprovedRequests = document.getElementById('mApprovedRequests');
let mDeniedRequests = document.getElementById('mDeniedRequests');

let aTotalRequests = document.getElementById('aTotalRequests');
let aPendingRequests = document.getElementById('aPendingRequests');
let aApprovedRequests = document.getElementById('aApprovedRequests');
let aDeniedRequests = document.getElementById('aDeniedRequests');

let mTotal = document.getElementById('mTotal');
let mPending = document.getElementById('mPending');
let mApproved = document.getElementById('mApproved');
let mDenied = document.getElementById('mDenied');

let aTotal = document.getElementById('aTotal');
let aPending = document.getElementById('aPending');
let aApproved = document.getElementById('aApproved');
let aDenied = document.getElementById('aDenied');

let tableHolder = document.getElementById('tableHolder');

let actBtn = 1;
let denyBtn = 1;
let tableSelector = 0;
let tableCount = 0;

setCards(
    mTotalRequests,mPendingRequests,mApprovedRequests,mDeniedRequests,
    aTotalRequests, aPendingRequests, aApprovedRequests, aDeniedRequests
    );

    setInterval(function(){
        setCards(mTotalRequests,mPendingRequests,mApprovedRequests,mDeniedRequests, aTotalRequests, aPendingRequests, aApprovedRequests, aDeniedRequests); 
    }, 5000);

$.post(
    'http://127.0.0.1:3000/mTotal',
    function(result){
        tableSelector = 3;
        renderTable(1, result);
    }
)

function setCards(ele1, ele2, ele3, ele4, ele5, ele6, ele7, ele8){
    $.post(
        "http://127.0.0.1:3000/reqCards",
        function(result){
            ele1.innerText = result[0];
            ele2.innerText = result[1];
            ele3.innerText = result[2];
            ele4.innerText = result[3];

            ele5.innerText = result[4];
            ele6.innerText = result[5];
            ele7.innerText = result[6];
            ele8.innerText = result[7];
        }
    );
}


mTotal.addEventListener('click', ()=>{
    // console.log(1);
    $.post(
        'http://127.0.0.1:3000/mTotal',
        function(result){
            tableSelector = 3;
            tableCount = 1;
            renderTable(1, result);
        }
    )

})
mPending.addEventListener('click', ()=>{
    // console.log(2);
    $.post(
        'http://127.0.0.1:3000/mPending',
        function(result){
            tableSelector = 1;
            tableCount = 2;
            renderTable(1, result);
        }
    )
})
mApproved.addEventListener('click', ()=>{
    // console.log(3);
    $.post(
        'http://127.0.0.1:3000/mApproved',
        function(result){
            tableSelector = 3;
            tableCount = 3;
            renderTable(1, result);
        }
    )
})
mDenied.addEventListener('click', ()=>{
    // console.log(4);
    $.post(
        'http://127.0.0.1:3000/mDenied',
        function(result){
            tableSelector = 3;
            tableCount = 4;
            renderTable(1, result);
        }
    )
})


aTotal.addEventListener('click', ()=>{
    // console.log(5);
    $.post(
        'http://127.0.0.1:3000/aTotal',
        function(result){
            tableSelector = 3;
            tableCount = 5;
            renderTable(2, result);
        }
    )
})
aPending.addEventListener('click', ()=>{
    // console.log(6);
    $.post(
        'http://127.0.0.1:3000/aPending',
        function(result){
            tableSelector = 2;
            tableCount = 6;
            renderTable(2, result);
        }
    )
})
aApproved.addEventListener('click', ()=>{
    // console.log(7);
    $.post(
        'http://127.0.0.1:3000/aApproved',
        function(result){
            tableSelector = 3;
            tableCount = 7;
            renderTable(2, result);
        }
    )
})
aDenied.addEventListener('click', ()=>{
    // console.log(8);
    $.post(
        'http://127.0.0.1:3000/aDenied',
        function(result){
            tableSelector = 3;
            tableCount = 8;
            renderTable(2, result);
        }
    )  
})

function renderTable(headerVal, result){
    let arr1 = ['Serial no.', 'asset id', 'starting point', 'destination', 'date', 'time', 'custodian name', 'custodian id', 'requestor name', 'requestor id', 'request status', 'Actions'];
    let arr2 = ['Serial no.','applicant name', 'applicant id', 'email', 'date', 'contact', 'request status', 'Actions'];
    let arr3 = ['Serial no.','asset id', 'starting point', 'destination', 'date', 'time', 'custodian name', 'custodian id', 'requestor name', 'requestor id', 'request status'];
    let arr4 = ['Serial no.','applicant name', 'applicant id', 'email', 'date', 'contact', 'request status'];
    let arr = [];

    if(headerVal == 1 && tableSelector == 1){
        arr = arr1;
    }
    else if(headerVal == 2 && tableSelector == 2){
        arr = arr2;
    }
    else if(headerVal == 1 && (tableSelector != 1 || tableSelector != 2)){
        arr = arr3;
    }
    else if(headerVal == 2 && (tableSelector != 1 || tableSelector != 2)){
        arr = arr4;
    }

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
            row.insertCell(i).innerText = Object.values(result[x])[i];
        } 
        if(tableSelector == 1 || tableSelector == 2){
        let btn1 = document.createElement('button');
        btn1.innerText = 'Approve';
        btn1.className = 'approve';
        let btn2 = document.createElement('button');
        btn2.innerText = 'Deny';
        btn2.className = 'deny';
        row.insertCell(Object.values(result[x]).length).append(btn1, btn2);
        }
    }
    table.append(thead);
    table.append(tbody);
    tableHolder.append(table);
    actBtn = 1;
    denyBtn = 1;
    approveButton();
    denyButton();
    // let test = document.querySelectorAll('table tbody tr');
    // let ind = test[0].children.length-1;
    // console.log(test[1].children[ind].innerText);
}

function approveButton(){
    if(actBtn == 1){
        $('.approve').click(function(){
             console.log('fired approveButton');
            actBtn = 0;
            denyBtn = 0;
            this.nextElementSibling.style.display = 'none';
            if(tableSelector == 1){
                // let len = this.parentElement.parentElement.children.length;
                // let id = this.parentElement.parentElement.children[0].innerText;
                // let serial = this.parentElement.parentElement.children[len-2].innerText;
                let serial = this.parentElement.parentElement.children[0].innerText;
                let id = this.parentElement.parentElement.children[1].innerText;
                $.post(
                    "http://127.0.0.1:3000/mAppr",
                    {
                        reqID : id,
                        reqSerial : serial                        
                    },
                    function(result){
                        console.log(result);
                    }
                )
            }
            else if(tableSelector == 2){
                // let len = this.parentElement.parentElement.children.length;
                // let serial = this.parentElement.parentElement.children[len-2].innerText;
                // id = this.parentElement.parentElement.children[1].innerText;
                let serial = this.parentElement.parentElement.children[0].innerText;
                let userName = this.parentElement.parentElement.children[1].innerText;
                let id = this.parentElement.parentElement.children[2].innerText;                
                let email = this.parentElement.parentElement.children[3].innerText;
                console.log(id);
                $.post(
                    "http://127.0.0.1:3000/aAppr",
                    {
                        reqID : id,
                        reqSerial : serial,
                        userName : userName,
                        email : email
                    },
                    function(result){
                        console.log(result);
                    }
                )
            }
        })
    }
}

function denyButton(){
    if(denyBtn == 1){
        $('.deny').click(function(){
             console.log('fired denyButton');
            this.previousElementSibling.style.display = 'none';
            if(tableSelector == 1){
                // let len = this.parentElement.parentElement.children.length;
                // let serial = this.parentElement.parentElement.children[len-2].innerText;
                let serial = this.parentElement.parentElement.children[0].innerText;
                let id = this.parentElement.parentElement.children[1].innerText;

                $.post(
                    "http://127.0.0.1:3000/mdeny",
                    {
                        reqID : id,
                        reqSerial : serial
                    },
                    function(result){
                        console.log(result);
                    }
                )
            }
            else if(tableSelector == 2){
                let serial = this.parentElement.parentElement.children[0].innerText;
                let id = this.parentElement.parentElement.children[2].innerText;
                $.post(
                    "http://127.0.0.1:3000/adeny",
                    {
                        reqID : id,
                        reqSerial : serial
                    },
                    function(result){
                        console.log(result);
                    }
                )
            }
        })
    }
}

