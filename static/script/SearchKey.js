

/*
* 函数: makeTree
* 注释: 将关键字生成一颗树
*/
function makeTree(objKeys) {
    var strKeys = objKeys;
    var arrKeys = strKeys.split("");
    var tblRoot = {};
    var tblCur = tblRoot;
    var key;

    for (var i = 0, n = arrKeys.length; i < n; i++) {
        key = arrKeys[i];

        if (key == ';')		//完成当前关键字
        {
            tblCur.end = true;
            tblCur = tblRoot;
            continue;
        }

        if (key in tblCur)	//生成子节点
            tblCur = tblCur[key];
        else
            tblCur = tblCur[key] = {};
    }

    tblCur.end = true; 	//最后一个关键字没有分割符

    return tblRoot;
}

/*
* 函数: search
* 注释: 找出关键字
*/
function search(content, tblRoot) {
    var tblCur;
    var i = 0;
    var n = content.length;
    var p, v;
    var arrMatch = [];

    while (i < n) {
        tblCur = tblRoot;
        p = i;
        v = 0;

        for (; ;) {
            if (!(tblCur = tblCur[content.charAt(p++)])) {
                i++;
                break;
            }

            if (tblCur.end)		//找到匹配关键字
                v = p;
        }

        if (v)					//最大匹配
        {
            arrMatch.push(content.substring(i - 1, v));
            i = v;
        }
    }

    arrMatch = unique(arrMatch);

    return arrMatch;
}

/*
* 函数: unique
* 注释: 去除重复
*/
function unique(arr) {
    var result = [], hash = {};
    for (var i = 0, elem; (elem = arr[i]) != null; i++) {
        if (!hash[elem]) {
            result.push(elem);
            hash[elem] = true;
        }
    }
    return result;
}
