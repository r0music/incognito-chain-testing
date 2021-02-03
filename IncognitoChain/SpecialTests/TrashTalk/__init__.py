RPC_METHODS = [
    "testrpcserver",
    "startprofiling",
    "stopprofiling",
    "exportmetrics",
    "getnetworkinfo",
    "getconnectioncount",
    "getallconnectedpeers",
    "getallpeers",
    "getnoderole",
    "getinoutmessages",
    "getinoutmessagecount",
    "estimatefee",
    "estimatefeev2",
    "estimatefeewithestimator",
    "getactiveshards",
    "getmaxshardsnumber",
    "getmininginfo",
    "getrawmempool",
    "getnumberoftxsinmempool",
    "getmempoolentry",
    "removetxinmempool",
    "getbeaconpoolstate",
    "getshardpoolstate",
    "getshardpoollatestvalidheight",
    "getshardtobeaconpoolstate",
    "getcrossshardpoolstate",
    "getnextcrossshard",
    "getshardtobeaconpoolstatev2",
    "getcrossshardpoolstatev2",
    "getshardpoolstatev2",
    "getbeaconpoolstatev2",
    "getfeeestimator",
    "setbackup",
    "getlatestbackup",
    "getbestblock",
    "getbestblockhash",
    "getblocks",
    "retrieveblock",
    "retrieveblockbyheight",
    "retrievebeaconblock",
    "retrievebeaconblockbyheight",
    "getblockchaininfo",
    "getblockcount",
    "getblockhash",
    "listoutputcoins",
    "createtransaction",
    "sendtransaction",
    "createandsendtransaction",
    "createandsendtransactionv2",
    "createandsendcustomtokentransaction",
    "sendrawcustomtokentransaction",
    "createrawcustomtokentransaction",
    "createrawprivacycustomtokentransaction",
    "sendrawprivacycustomtokentransaction",
    "createandsendprivacycustomtokentransaction",
    "createandsendprivacycustomtokentransactionv2",
    "getmempoolinfo",
    "getpendingtxsinblockgen",
    "getcandidatelist",
    "getcommitteelist",
    "canpubkeystake",
    "gettotaltransaction",
    "listunspentcustomtoken",
    "getbalancecustomtoken",
    "gettransactionbyhash",
    "gettransactionhashbyreceiver",
    "gettransactionhashbyreceiverv2",
    "gettransactionbyreceiver",
    "gettransactionbyreceiverv2",
    "listcustomtoken",
    "listprivacycustomtoken",
    "getprivacycustomtoken",
    "listprivacycustomtokenbyshard",
    "getbalanceprivacycustomtoken",
    "customtoken",
    "customtokenholder",
    "privacycustomtoken",
    "checkhashvalue",
    "getlistcustomtokenbalance",
    "getlistprivacycustomtokenbalance",
    "getheader",
    "getcrossshardblock",
    "randomcommitments",
    "hasserialnumbers",
    "hassnderivators",
    "listsnderivators",
    "listserialnumbers",
    "listcommitments",
    "listcommitmentindices",
    "createandsendstakingtransaction",
    "createandsendstakingtransactionv2",
    "createandsendstopautostakingtransaction",
    "createandsendstopautostakingtransactionv2",
    "decryptoutputcoinbykeyoftransaction",
    "getandsendtxsfromfile",
    "getandsendtxsfromfilev2",
    "unlockmempool",
    "getautostakingbyheight",
    "getcommitteestate",
    "getrewardamountbyepoch",
    "getshardbeststate",
    "getshardbeststatedetail",
    "getbeaconbeststate",
    "getbeaconbeststatedetail",
    "listaccounts",
    "getaccount",
    "getaddressesbyaccount",
    "getaccountaddress",
    "dumpprivkey",
    "importaccount",
    "removeaccount",
    "listunspentoutputcoins",
    "getbalance",
    "getbalancebyprivatekey",
    "getbalancebypaymentaddress",
    "getreceivedbyaccount",
    "settxfee",
    "getpublickeyfrompaymentaddress",
    "defragmentaccount",
    "defragmentaccountv2",
    "defragmentaccounttoken",
    "defragmentaccounttokenv2",
    "getstackingamount",
    "hashtoidenticon",
    "generatetokenid",
    "createissuingrequest",
    "sendissuingrequest",
    "createandsendissuingrequest",
    "createandsendissuingrequestv2",
    "createandsendcontractingrequest",
    "createandsendcontractingrequestv2",
    "createandsendburningrequest",
    "createandsendburningrequestv2",
    "createandsendtxwithissuingethreq",
    "createandsendtxwithissuingethreqv2",
    "checkethhashissued",
    "getallbridgetokens",
    "getethheaderbyhash",
    "getbridgereqwithstatus",
    "getbeaconswapproof",
    "getlatestbeaconswapproof",
    "getbridgeswapproof",
    "getlatestbridgeswapproof",
    "getburnproof",
    "withdrawreward",
    "getrewardamount",
    "getrewardamountbypublickey",
    "listrewardamount",
    "revertbeaconchain",
    "revertshardchain",
    "enablemining",
    "getchainminingstatus",
    "getpublickeymining",
    "getpublickeyrole",
    "getrolebyvalidatorkey",
    "getincognitopublickeyrole",
    "getminerrewardfromminingkey",
    "getproducersblacklist",
    "getproducersblacklistdetail",
    "getpdestate",
    "createandsendtxwithwithdrawalreq",
    "createandsendtxwithwithdrawalreqv2",
    "createandsendtxwithpdefeewithdrawalreq",
    "createandsendtxwithptokentradereq",
    "createandsendtxwithptokencrosspooltradereq",
    "createandsendtxwithprvtradereq",
    "createandsendtxwithprvcrosspooltradereq",
    "createandsendtxwithptokencontribution",
    "createandsendtxwithprvcontribution",
    "createandsendtxwithptokencontributionv2",
    "createandsendtxwithprvcontributionv2",
    "convertnativetokentoprivacytoken",
    "convertprivacytokentonativetoken",
    "getpdecontributionstatus",
    "getpdecontributionstatusv2",
    "getpdetradestatus",
    "getpdewithdrawalstatus",
    "getpdefeewithdrawalstatus",
    "convertpdeprices",
    "extractpdeinstsfrombeaconblock",
    "getburningaddress",
    "createandsendtxwithcustodiandeposit",
    "createandsendtxwithreqptoken",
    "getportalstate",
    "getportalcustodiandepositstatus",
    "createandsendregisterportingpublictokens",
    "createandsendportalexchangerates",
    "getportalfinalexchangerates",
    "getportalportingrequestbykey",
    "getportalportingrequestbyportingid",
    "convertexchangerates",
    "getportalreqptokenstatus",
    "getportingrequestfees",
    "createandsendtxwithredeemreq",
    "createandsendtxwithrequnlockcollateral",
    "getportalrequnlockcollateralstatus",
    "getportalreqredeemstatus",
    "createandsendcustodianwithdrawrequest",
    "getcustodianwithdrawbytxid",
    "getcustodianliquidationstatus",
    "createandsendtxwithreqwithdrawrewardportal",
    "createandsendredeemliquidationexchangerates",
    "createandsendliquidationcustodiandeposit",
    "createandsendtopupwaitingporting",
    "getamountneededforcustodiandepositliquidation",
    "getliquidationtpexchangeratespool",
    "getportalreward",
    "getrequestwithdrawportalrewardstatus",
    "createandsendtxwithreqmatchingredeem",
    "getreqmatchingredeemstatus",
    "getcustodiantopupstatus",
    "getcustodiantopupwaitingportingstatus",
    "getamounttopupwaitingporting",
    "getreqredeemstatusbytxid",
    "getreqredeemfromliquidationpoolbytxidstatus",
    "createandsendtxwithrelayingbnbheader",
    "createandsendtxwithrelayingbtcheader",
    "getrelayingbnbheaderstate",
    "getrelayingbnbheaderbyblockheight",
    "getbtcrelayingbeststate",
    "getbtcblockbyhash",
    "getlatestbnbheaderblockheight",
    "getburnprooffordeposittosc",
    "createandsendburningfordeposittoscrequest",
    "createandsendburningfordeposittoscrequestv2",
    "getbeaconpoolinfo",
    "getshardpoolinfo",
    "getcrossshardpoolinfo",
    "getallview",
    "getallviewdetail",
    "getrewardfeature",
    "gettotalstaker",
    "getvalkeystate",
]
