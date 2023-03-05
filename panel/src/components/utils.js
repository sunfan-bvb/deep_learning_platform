// 是否具有该线
import Vue from 'vue'
export default new Vue

export function hasLine(data, from, to) {
    for (let i = 0; i < data.lineList.length; i++) {
        let line = data.lineList[i]
        if (line.from === from && line.to === to) {
            return true
        }
    }
    return false
}

// 是否含有相反的线
export function hashOppositeLine(data, from, to) {
    return hasLine(data, to, from)
}

// 获取连线
export function getConnector(jsp, from, to) {
    let connection = jsp.getConnections({
        source: from,
        target: to
    })[0]
    return connection
}

// 获取唯一标识
export function uuid() {
    return Math.random().toString(36).substr(3, 10)
}

export function save_log(op){
    console.log(op)
    var time = new Date()
    Vue.prototype.$http.post("http://59.77.17.71:5001/saveinfolog", {date: time.toLocaleDateString(), op: op, time: time.toLocaleTimeString()})
}

export function run_log(str){
    console.log(str)
    var time = new Date()
    Vue.prototype.$http.post("http://59.77.17.71:5001/saveinfolog", {date: time.toLocaleDateString(), str: str, time: time.toLocaleTimeString()})
}