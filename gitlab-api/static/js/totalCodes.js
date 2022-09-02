/*!
 对table表单的新增代码列进行求和
 author : gibson
*/
function totalCodes(target_id, cell_num, ignore_first_row){
    let table = document.getElementById(target_id);
    let sum = 0;
    for(let i = 0; i < table.rows.length; i++){
        //获取制定列的值
        let val = table.rows[i].cells[cell_num-1].innerText;
        //转成浮点数进行运算
        val = parseFloat(val);
        //第一行的情况下
        if(i==0){
            //不忽略第一行（第一行不是表头）就累加
            if(!ignore_first_row){
                sum += val;
            }
        }else{
            //累加
            sum += val;
        }
    }
    return sum;
}

//获取table中第4列的值的和
let sum = totalCodes('table', 4, true);
console.log("合计：" + sum);