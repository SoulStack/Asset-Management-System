const express = require("express");
const cors = require('cors');
const mssql = require('mssql');
const nodeMailer = require('nodemailer');
let moment = require('moment');
let app = express();
/*
app.use(express.urlencoded({extended:false}));

app.use(
    cors({
        origin : '10.0.175.122',
        methods: ['GET', 'POST', 'PUT', 'DELETE'],
        allowHeaders : ['Content-Type']
    })
);
*/

app.use(function(req, res, next){
	res.header("Access-Control-Allow-Origin", "*");
});


const sqlConfig = {
    server : '10.0.175.122',
    user : 'SA',
    password : 'Soulsvciot01',
    database : 'asset',

    options: {
        encrypt : false,
        trustServerCertificate : false
    }
}

mssql.connect(sqlConfig, (err, result)=>{
    if(err) throw err
    else{
        console.log('connected to db');     
    }
})

let transporter = nodeMailer.createTransport({
    service : 'gmail',
    auth :{
        user : 'sayantanghosh1666@gmail.com',
        pass : 'washbox222'
    }
});

app.listen(3000);

// Landing page


app.post('/access', (req, res) =>{
    let appName = req.body.appName;
    let appID = req.body.appID;
    let appEmail = req.body.appEmail;
    let appContact = req.body.appContact;
    let firstName = appName.split(" ")[0];
    let lastName = appName.split(" ")[1];
    // console.log(appName);
    // console.log('Pass');

    // console.log(query1);
    let query1 = `SELECT * FROM Employees WHERE emp_no =` + 
                 `'${appID}'`+
                 `AND first_name =` +
                 `'${firstName}'` +
                 `AND last_name =` +
                 `'${lastName}'`;
    // console.log(query1);

    let queryResult1 = mssql.query(query1, (err1, result1) =>{
        if(err1){
            console.log('query1 failed');
            res.send('0');
        }
        else if(result1.recordset.length > 0){
            let query2 = `INSERT INTO Access_request(applicant_name, applicant_id, email, date, contact) values(` +
                          `'${appName}',` +
                          `'${appID}',` +
                          `'${appEmail}',` +
                          `'${moment().format('YYYY-MM-DD')}',` +
                          `'${appContact}'` + `)`;
            // console.log(query2);
            let queryResult2 = mssql.query(query2,(err2, result2)=>{
                if(err2){
                    // console.log('query2 failed');
                    res.send('0');
                }
                else{
                    let mailOptions1 = {
                        from : 'sayantanghosh1666@gmail.com',
                        to : '1804407@kiit.ac.in',
                        subject : 'Access request alert',
                        text : `${appName} with ID: ${appID} has requested access to the system. If needed kindly contact the applicant at ${appEmail} or ${appContact}`
                    }

                    let mailOptions2 = {
                        from : 'sayantanghosh1666@gmail.com',
                        to : 'sayantansnt@gmail.com',
                        subject : 'Access request alert',
                        text : `Request received. Our team will get in touch with you at the earliest regarding this`
                    }

                    transporter.sendMail(mailOptions1, (err, data)=>{
                        if(err) console.log('failed to send the mail 1');
                        else console.log('Mail sent');
                    });

                    transporter.sendMail(mailOptions2, (err, data)=>{
                        if(err) console.log('failed to send the mail 2');
                        else console.log('Mail sent');
                    })
                    res.send('1');
                }
            })
        }
        else{
            res.send('0');
        }
    })

}); // end of access

app.post('/login', (req, res)=>{
	console.log('request received');
    let userEmail = req.body.userEmail;
    let userPass = req.body.userPass;

    let query3 = `SELECT  * FROM Users WHERE email =` +
                `'${userEmail}'` +
                `AND password =` +
                `'${userPass}'`;
    console.log(query3);
    let queryResult3 = mssql.query(query3, (err3, result3)=>{
        if(err3){
            console.log('query3 failed');
            res.send('0');
        }
        else if(result3.recordset.length > 0){
            res.send('./dashboard.html');
        }
        else{
            res.send('0');
        }
    })
}) // end of login request

app.post('/asset', (req, res)=>{
    let reqName = req.body.reqName;
    let reqID = req.body.reqID;
    let assetID = req.body.assetID;
    let assetDept = req.body.assetDept;
    let source = req.body.source;
    let destination = req.body.destination;
    let firstName = reqName.split(" ")[0];
    let lastName = reqName.split(" ")[1];

    console.log(reqName);
    console.log(reqID);
    console.log(assetDept);
    console.log(assetID);
    console.log(source);
    console.log(destination);
    console.log(firstName);
    console.log(lastName);
    console.log('-----------------------------------------------');

    // Code '0' -> query failure 
    // Code '1' -> condition not satisfied
    // Code '2' -> condition satisfied
    // Code '3' -> auxillery message for condition not satified
    
    let query1 = `SELECT * FROM Movement_request WHERE asset_id = '${assetID}' AND Request_status = 'Pending'`;
    let query2 = `SELECT approve_status from Activity INNER JOIN assets ON assets.tag_id=Activity.tag_id where asset_id='${assetID}'`;
    let query3 = `SELECT room_name from rooms INNER JOIN assets ON assets.room_id=rooms.room_id where asset_id='${assetID}'`;
    let query4 = `SELECT * FROM Employees WHERE emp_no =` + `'${reqID}'` + `AND first_name = ` + `'${firstName}'` + `AND last_name = ` + `'${lastName}'`;
    let query5 = `SELECT * FROM assets WHERE asset_id =` + `'${assetID}'` + `AND asset_dept =` + `'${assetDept}'`;
    let query6 = `SELECT * FROM rooms WHERE room_name =` + `'${source}'` + 'OR room_name = ' + `'${destination}'`; 
    let query7 = `INSERT INTO Movement_request(asset_id, starting_point, destination, date, time, requester_name, requester_id) values(` +
                 `'${assetID}',` +
                 `'${source}',` +
                 `'${destination}',` +
                 `'${moment().format('YYYY-MM-DD')}',` +
                 `'${moment().format('hh:mm:ss')}',` +
                 `'${reqName}',` +
                 `'${reqID}'` + `)`;
    
    let queryResult1 = mssql.query(query1 , (err1, result1)=>{
        if(err1){
            console.log('/asset error 1');
            res.send('0');
        }
        else{
            if(result1.recordset.length > 0){
                res.send('1'); // unresolved request for the asset already exists
            }
            else{
                console.log('passed first query');
                let queryResult2 = mssql.query(query2, (err2, result2)=>{
                    if(err2){
                        console.log('/asset error 2')
                        res.send('0');
                    }
                    else{
                        if(Object.values(result2.recordset[0])[0] == 'True'){
                            res.send('1'); // the asset the request refers to is on the move 
                        }
                        else if(Object.values(result2.recordset[0])[0] == 'False'){
                            let queryResult3 = mssql.query(query3, (err3, result3)=>{
                                if(err3) console.log('/asset error 3')
                                else if(destination == Object.values(result3.recordset[0])[0]){
                                    res.send('3'); // the destination of the current request and the current location of the asset it concerns are same
                                }
                                else{
                                    //  rename query variable
                                    let queryResult4 = mssql.query(query4, (err4, result4)=>{
                                        if(err4){
                                            console.log('query4 failed');
                                            res.send('0');
                                        }
                                        else if(result4.recordset.length > 0){
                                            let queryResult5 = mssql.query(query5, (err5, result5)=>{
                                                if(err5){
                                                    console.log('query5 failed');
                                                    res.send('0');
                                                }
                                                else if(result5.recordset.length > 0){
                                                    let queryResult6 = mssql.query(query6, (err6, result6)=>{
                                                        if(err6){
                                                            console.log('query6 failed');
                                                            res.send('0');
                                                        }
                                                        else if(result6.recordset.length > 0){
                                                            // console.log(result3.recordset);
                                                            let queryResult7 = mssql.query(query7, (err7, result7)=>{
                                                                if(err7){
                                                                    console.log('query7 failed');
                                                                    res.send('0'); 
                                                                }
                                                                else{
                                                                    res.send('2');
                                                                    console.log('success');
                                                                }
                                                            })
                                                        }
                                                        else{
                                                            res.send('1');
                                                            console.log('no matching records found 3');
                                                        }
                                                    })
                                                }
                                                else{
                                                    res.send('1');
                                                    console.log('no matching records found 2');
                                                }
                                            })
                                        }
                                        else{
                                            res.send('1');
                                            console.log('no matching records found 1');
                                        }
                                    })
                                }
                            })
                        }
                    }
                })
            }
        }
    })
})

app.post('/contact',(req, res)=>{
    let visitorName = req.body.visitorName;
    let visitorID = req.body.visitorID;
    let visitorMsg = req.body.visitorMsg;

    let mailOptions1 = {
        from : 'sayantanghosh1666@gmail.com',
        to : 'sayantansnt@gmail.com',
        subject : 'System issue report received',
        text : `Thank you for contacting us. We have received your query and our staff will reach out to you at the earlies possible moment`
    }

    let mailOptions2 = {
        from : `sayantanghosh1666@gmail.com`,
        to : `1804407@kiit.ac.in`,
        subject : 'System issue report',
        text : `Name : ${visitorName}, employee ID : ${visitorID}. Report : ${visitorMsg}`
    }

    transporter.sendMail(mailOptions1, (err, data)=>{
        if(err) console.log('failed to send the mail 2');
        else console.log('Mail sent');
    })
    transporter.sendMail(mailOptions2, (err, data)=>{
        if(err) console.log('failed to send the mail 2');
        else console.log('Mail sent');
    })
})

// Dashboard page

app.post('/setCards', (req, res)=>{
    let arr = [];
    let dquery1 = `SELECT count(*) from assets`;
    let dquery2 = `SELECT count(*) from assets INNER JOIN Activity ON Activity.tag_id=assets.tag_id where approve_status='False'`;
    let dquery3 = `SELECT count(*) from assets INNER JOIN Activity ON Activity.tag_id=assets.tag_id where movement_status='True'`;
    let dquery4 = `SELECT count(*) from tags`;
    let dquery5 = `SELECT count(*) from tags INNER JOIN assets ON assets.tag_id=tags.tag_id where assets.asset_id IS NULL`;
    let dquery6 = `SELECT count(*) from tags INNER JOIN assets ON assets.tag_id=tags.tag_id where assets.asset_id IS NOT NULL`;
    let dquery7 = `SELECT count(*) from reader`;
    let dquery8 = `SELECT count(*) from reader where reader_status='Connected'`;
    let dquery9 = `SELECT count(*) from reader where reader_status='Disconnected'`;
    // console.log(dquery1);
    let queryResult1 = mssql.query(`SELECT count(*) from assets`, (derr1, result1)=>{
        if(derr1) {
            console.log('dash query 1 failed');
            // console.log(err1);
        }
        else{
            // console.log(Object.values(result1.recordset[0])[0]);
            arr.push(Object.values(result1.recordset[0])[0]);
            // available assets
            let queryResult2 = mssql.query(dquery2, (err2, result2)=>{
              if(err2) throw err2  
              else{
                // console.log(Object.values(result2.recordset[0])[0]);
                arr.push(Object.values(result2.recordset[0])[0]); 
                 //assets on-move
                let queryResult3 = mssql.query(dquery3, (err3, result3)=>{
                    if(err3) throw err3
                    else{
                        // console.log(Object.values(result3.recordset[0])[0]);
                        arr.push(Object.values(result3.recordset[0])[0]);
                        
                        let queryResult4 = mssql.query(dquery4, (err4, result4)=>{
                            if(err4) throw err4
                            else{
                                // console.log(Object.values(result4.recordset[0])[0]);
                                arr.push(Object.values(result4.recordset[0])[0]);
                                
                                let queryResult5 = mssql.query(dquery5, (err5, result5)=>{
                                    if(err5) throw err5
                                    else{
                                        // console.log(Object.values(result5.recordset[0])[0]);
                                        arr.push(Object.values(result5.recordset[0])[0]);
                                        
                                        let queryResult6 = mssql.query(dquery6, (err6, result6)=>{
                                            if(err6) throw err6
                                            else{
                                                // console.log(Object.values(result6.recordset[0])[0]);
                                                arr.push(Object.values(result6.recordset[0])[0]);
                                                
                                                let queryResult7 = mssql.query(dquery7, (err7, result7)=>{
                                                    if(err7) throw err7
                                                    else{
                                                        // console.log(Object.values(result7.recordset[0])[0]);
                                                        arr.push(Object.values(result7.recordset[0])[0]);
                                                        let query8 = ``;
                                                        let queryResult8 = mssql.query(dquery8, (err8, result8)=>{
                                                            if(err8) throw err8
                                                            else{
                                                                // console.log(Object.values(result8.recordset[0])[0]);
                                                                arr.push(Object.values(result8.recordset[0])[0]);
                                                                
                                                                let queryResult9 = mssql.query(dquery9, (err9, result9)=>{
                                                                    if(err9) throw err9
                                                                    else{
                                                                        // console.log(Object.values(result9.recordset[0])[0]);
                                                                        arr.push(Object.values(result9.recordset[0])[0]);
                                                                        // console.log(arr);
                                                                        res.send(arr);
                                                                    }
                                                                }) // end of query 9
                                                            }
                                                        }) // end of query 8
                                                    }
                                                }) // end of query 7
                                            }
                                        }) // end of query 6
                                    }
                                }) // end of query 5
                            }
                        }) // end of query 4
                    }
                }) // end of query 3
              }
            }) // end of query 2
        }
    })// end of query 1
})


app.post('/getChartData', (req, res) =>{
    let arr = [
        [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120],
        [120, 110, 100, 90, 80, 70, 60, 50, 40, 30, 20, 10]
    ];
    res.send(arr);
});
app.post('/setTable', (req, res) =>{

    let query = `SELECT TOP (20) * From Movement_request`;
    let queryResult = mssql.query(query, (err, result)=>{
        if(err) throw err;
        else{
            res.send(result.recordset);
        }
    });
    // let obj = [
    //     {field1 : 'field1', field2 : 'field2', field3 : 'field3', field4 : 'field4', field5 : 'field5'},
    //     {field1 : 'field1', field2 : 'field2', field3 : 'field3', field4 : 'field4', field5 : 'field5'},
    //     {field1 : 'field1', field2 : 'field2', field3 : 'field3', field4 : 'field4', field5 : 'field5'}
    // ];
    // res.send(obj);
});


app.post('/getTileData', (req, res) =>{
    let query = `SELECT DISTINCT asset_dept,count(asset_id) AS 'num'
        FROM assets
        INNER JOIN Activity ON Activity.tag_id=assets.tag_id
        where Activity.approve_date between '2010-02-20' and '2099-02-24'
        GROUP BY asset_dept`;
        
        let queryResult = mssql.query(query, (err, result) => {
            let dept = [];
            let perDept = [];
            let arr = [];
            set = result.recordset;
            console.log(set);
            for(x in set){
                dept.push(set[x].asset_dept);
            }
            // console.log(dept);
            for(x in set){
                perDept.push(set[x].num);
            }
            // console.log(perDept);

            arr.push(dept, perDept);
            // console.log(arr);
            res.send(arr);
        });
});
app.post('/getPerformanceData', (req, res) =>{
    let spec = [];
    let specValue = [];
    let performance = [];
        let query = `SELECT TOP 1 * FROM Performance`;
        let queryResult = mssql.query(query, (err, result) => {
            spec = Object.keys(result.recordset[0]);
            specValue = Object.values(result.recordset[0]);

            performance.push(spec, specValue);
            res.send(performance);
        });
});



// Alerts

app.post('/alertCard', (req, res)=>{
    let query = `SELECT count(*) from Alert`;
    let queryResult = mssql.query(query, (err, result)=>{
        if(err) throw err
        else{
            // console.log(result);
            // console.log(Object.values(result.recordset[0])[0]);
            res.send(Object.values(result.recordset[0])[0].toString());
        }
    })
});

app.post('/totalAlertsTable', (req, res)=>{
    let query = `SELECT * FROM Alert`;
    let queryResult = mssql.query(query, (err, result)=>{
        res.send(result.recordset);
    })
})

// requests

app.post('/reqCards',(req, res)=>{
    let arr = [];
    let query1 = `SELECT count(*) from Movement_request`;
    let query2 = `SELECT count(*) from Movement_request where Request_status = 'Pending'`;
    let query3 = `SELECT count(*) from Movement_request where Request_status = 'Approved'`;
    let query4 = `SELECT count(*) from Movement_request where Request_status = 'Denied'`;
    let query5 = `SELECT count(*) from Access_request`;
    let query6 = `SELECT count(*) from Access_request where Request_status = 'Pending'`;
    let query7 = `SELECT count(*) from Access_request where Request_status = 'Approved'`;
    let query8 = `SELECT count(*) from Access_request where Request_status = 'Denied'`;

    let queryResult1 = mssql.query(query1, (err1, result1)=>{
        if(err1) throw err1
        else{
            arr.push(Object.values(result1.recordset[0])[0]);
            let queryResult2 = mssql.query(query2, (err2, result2)=>{
                if(err2) throw err2
                else{
                    arr.push(Object.values(result2.recordset[0])[0]);
                    let queryResult3 = mssql.query(query3, (err3, result3)=>{
                        if(err3) throw err3
                        else{
                            arr.push(Object.values(result3.recordset[0])[0]);  
                            let queryResult4 = mssql.query(query4, (err4, result4)=>{
                                if(err4) throw err4
                                else{
                                    arr.push(Object.values(result4.recordset[0])[0]);  
                                    let queryResult5 = mssql.query(query5, (err5, result5)=>{
                                        if(err5) throw err5
                                        else{
                                            arr.push(Object.values(result5.recordset[0])[0]);  
                                            let queryResult6 = mssql.query(query6, (err6, result6)=>{
                                                if(err6) throw err6
                                                else{
                                                    arr.push(Object.values(result6.recordset[0])[0]); 
                                                    let queryResult7 = mssql.query(query7, (err7, result7)=>{
                                                        if(err7) throw err7
                                                        else{
                                                            arr.push(Object.values(result7.recordset[0])[0]); 
                                                            let queryResult8 = mssql.query(query8, (err8, result8)=>{
                                                                if(err8) throw err8
                                                                else{
                                                                    arr.push(Object.values(result8.recordset[0])[0]); 
                                                                    res.send(arr);
                                                                }
                                                        }) //q8
                                                    }  
                                                }) // q7
                                            }
                                        }) //q6
                                    }
                                }) //q5
                            } 
                        }) //q4
                    }
            }) //q3
        }
    }) //q2
        }
}) //q1
})
app.post('/mTotal', (req, res)=>{
    let query = `SELECT * from Movement_request`;
    let queryResult = mssql.query(query,(err, result)=>{
        if(err) throw err
        else{
            res.send(result.recordset);
        }
    });
})
app.post('/mPending', (req, res)=>{
    let query = `SELECT * from Movement_request where Request_status = 'Pending'`;
    let queryResult = mssql.query(query,(err, result)=>{
        if(err) throw err
        else{
            res.send(result.recordset);
        }
    });
})
app.post('/mApproved', (req, res)=>{
    let query = `SELECT * from Movement_request where Request_status = 'Approved'`;
    let queryResult = mssql.query(query,(err, result)=>{
        if(err) throw err
        else{
            res.send(result.recordset);
        }
    });
})
app.post('/mDenied', (req, res)=>{
    let query = `SELECT * from Movement_request where Request_status = 'Denied'`;
    let queryResult = mssql.query(query,(err, result)=>{
        if(err) throw err
        else{
            res.send(result.recordset);
        }
    });
})

app.post('/aTotal', (req, res)=>{
    let query = `SELECT * from Access_request`;
    let queryResult = mssql.query(query,(err, result)=>{
        if(err) throw err
        else{
            res.send(result.recordset);
        }
    });
})
app.post('/aPending', (req, res)=>{
    let query = `SELECT * from Access_request where Request_status = 'Pending'`;
    let queryResult = mssql.query(query,(err, result)=>{
        if(err) throw err
        else{
            res.send(result.recordset);
        }
    });
})
app.post('/aApproved', (req, res)=>{
   let query = `SELECT * from Access_request where Request_status = 'Approved'`;
    let queryResult = mssql.query(query,(err, result)=>{
        if(err) throw err
        else{
            res.send(result.recordset);
        }
    });
})
app.post('/aDenied', (req, res)=>{
    let query = `SELECT * from Access_request where Request_status = 'Denied'`;
    let queryResult = mssql.query(query,(err, result)=>{
        if(err) throw err
        else{
            res.send(result.recordset);
        }
    });
})


app.post('/mAppr', (req, res)=>{
    let id = req.body.reqID;
    let serial = req.body.reqSerial;
    console.log(serial);
    let q1 = `UPDATE Activity SET approve_status='True' from Activity INNER JOIN assets ON assets.tag_id=Activity.tag_id where asset_id='${id}'`;
    let q2 = `UPDATE Movement_request SET Request_status='Approved' from Movement_request where asset_id='${id}' AND serial = '${serial}'`;

    let queryResult1 = mssql.query(q1, (err1, result1)=>{
        if(err1) console.log('failed appr query1')
        else{
            let queryResult2 = mssql.query(q2, (err2, result2)=>{
                if(err2) console.log(err2)
                else{
                    res.send(id.toString());
                }
            })
        }
    })
})
app.post('/aAppr', (req, res)=>{
    let id = req.body.reqID;
    let serial = req.body.reqSerial;
    let userName = req.body.userName;
    let email = req.body.email;
    let pass = `user`;
    let q1 = `UPDATE Access_request SET Request_status='Approved' where serial='${serial}' and applicant_id='${id}'`;
    let q2 = `INSERT INTO Users(user_id,user_name,email,password)values(` + `'${id}',` + `'${userName}',` + `'${email}',` +  `'${[pass]}'` +`)`;

    let queryResult1 = mssql.query(q1,(err1, result1)=>{
        if(err1) throw err1
        else{
            let queryResult2 = mssql.query(q2, (err2, result2)=>{
                if(err2) throw err2
                else{
                    res.send('success');
                }
            })
        }
    })
})

app.post('/mdeny', (req, res)=>{
    let id = req.body.reqID;
    let serial = req.body.reqSerial;
    
    let q1 = `UPDATE Activity SET approve_status='False' from Activity INNER JOIN assets ON assets.tag_id=Activity.tag_id where asset_id='${id}'`;
    let q2 = `UPDATE Movement_request SET Request_status='Denied' from Movement_request where asset_id='${id}' AND serial = '${serial}'`;
    console.log(q2);
    let queryResult1 = mssql.query(q1, (err1, result1)=>{
        if(err1) console.log('failed deny query1')
        else{
            let queryResult2 = mssql.query(q2, (err2, result2)=>{
                if(err2) console.log('err2')
                else{
                    res.send(id.toString());
                }
            })
        }
    })
})
app.post('/aDeny', (req, res)=>{
    let q = `UPDATE Access_request SET Request_status='Denied' where serial='${serial}' and applicant_id='${id}'`;
    let queryResult = mssql.query(q, (err, result)=>{
        if(err) throw err
        else{
            res.send('Denied');
        }
    })
})
