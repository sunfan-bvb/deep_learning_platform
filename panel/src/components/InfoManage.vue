<template>
<div>
  <div class="title">用户管理</div>
   <el-tabs v-model="activeName" style="width: 80%; margin-left: 10%">
    <el-tab-pane label="用户管理" name="first">
      <div v-show="userTableShow">
      <el-input v-model="input" placeholder="请输入内容" style="width: 15vw"></el-input>
      <el-button type="primary" icon="el-icon-search" style="margin-left: 1vh" @click="search">搜索</el-button>
      <el-select v-model="value" placeholder="请选择" style="margin-left: 5vh" @change="selectChange">
          <el-option
            v-for="item in roleList"
            :key="item"
            :label="item"
            :value="item">
          </el-option>
        </el-select>
      <el-table
    ref="multipleTable"
    :data="tableData"
    style="width: 80vw;font-size: medium; margin-top: 2vw"
    max-height="400"
    @selection-change="handleSelectionChange">
    <el-table-column
      type="selection"
      width="70">
    </el-table-column>
    <el-table-column
      prop="id"
      label="编号"
      width="220">
    </el-table-column>
    <el-table-column
      prop="name"
      label="用户名"
      width="220">
    </el-table-column>
    <el-table-column
      prop="role"
      label="角色"
      width="220">
    </el-table-column>
    <el-table-column
      prop="state"
      label="使用状态"
      width="220">
    </el-table-column>
    <el-table-column
      label="操作"
      width="220">
      <template slot-scope="scope">
        <el-button
          @click.native.prevent="deleteRow(scope.$index, tableData)"
          type="text"
          style="color: red"
          size="small">
          移除
        </el-button>
        <el-button
          @click.native.prevent="editRow(scope.$index, tableData)"
          type="text"
          size="small">
          编辑
        </el-button>
        <el-button
          @click.native.prevent="disableRow(scope.$index, tableData)"
          type="text"
          size="small">
          {{tableData[scope.$index].state == "启用"? '禁用': '启用'}}
        </el-button>
      </template>
    </el-table-column>
  </el-table>
  <el-button type="primary" @click="toggleSelection()" style="margin-top: 2vh">取消选择</el-button>
  <el-button type="primary" @click="patchDelete()" style="margin-top: 2vh">批量删除</el-button>
  </div>
      <el-result icon="error" title="暂无权限" subTitle="您无权查看用户信息" v-show="!userTableShow">
      </el-result>
    </el-tab-pane>
    <el-tab-pane label="用户添加" name="second">
      <el-form :model="form" label-width="80px">
        <el-form-item label="用户名">
          <el-input v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="密码">
            <el-input v-model="form.password" type="password"></el-input>
        </el-form-item>
        <el-form-item label="角色">
          <el-radio-group v-model="form.role" v-for="role in realRoleList" :key="role">
              <el-radio :label="role" style="margin-right: 30px"></el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="状态">
          <el-radio-group v-model="form.state">
            <el-radio label="启用"></el-radio>
            <el-radio label="禁用"></el-radio>
          </el-radio-group>
        </el-form-item>
<!--        <span style="font-size: x-small; margin-left: 80px">*默认密码为123456</span>-->
        <el-form-item>
          <el-button type="primary" @click="onSubmit" style="margin-top: 3vh">添加用户</el-button>
          <el-button style="margin-top: 3vh" @click="reset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-tab-pane>
<!--     <el-tab-pane label="角色管理" name="third">-->
<!--      <el-input v-model="rolesearch" placeholder="请输入内容" style="width: 15vw"></el-input>-->
<!--      <el-button type="primary" icon="el-icon-search" style="margin-left: 1vh" @click="roleSearch">搜索</el-button>-->
<!--      <el-table-->
<!--          ref="roleTable"-->
<!--          :data="roleData"-->
<!--          style="width: 80vw;font-size: medium; margin-top: 2vw"-->
<!--          max-height="400"-->
<!--          @selection-change="handleRoleSelectionChange">-->
<!--          <el-table-column-->
<!--            type="selection"-->
<!--            width="100">-->
<!--          </el-table-column>-->
<!--          <el-table-column-->
<!--            prop="id"-->
<!--            label="编号"-->
<!--            width="350">-->
<!--          </el-table-column>-->
<!--          <el-table-column-->
<!--            prop="name"-->
<!--            label="角色名称"-->
<!--            width="350">-->
<!--          </el-table-column>-->
<!--          <el-table-column-->
<!--            label="操作"-->
<!--            width="350">-->
<!--            <template slot-scope="rolescope">-->
<!--              <el-button-->
<!--                @click.native.prevent="roleDeleteRow(rolescope.$index, roleData)"-->
<!--                type="text"-->
<!--                style="color: red"-->
<!--                size="small">-->
<!--                移除-->
<!--              </el-button>-->
<!--              <el-button-->
<!--                @click.native.prevent="roleEditRow(rolescope.$index, roleData)"-->
<!--                type="text"-->
<!--                size="small">-->
<!--                编辑-->
<!--              </el-button>-->
<!--            </template>-->
<!--          </el-table-column>-->
<!--        </el-table>-->
<!--        <el-button type="primary" @click="toggleRoleSelection()" style="margin-top: 2vh">取消选择</el-button>-->
<!--        <el-button type="primary" @click="patchRoleDelete()" style="margin-top: 2vh">批量删除</el-button>-->
<!--    </el-tab-pane>-->
    <el-tab-pane label="角色与权限管理" name="fifth">
      <div v-show="roleTableShow">
      <el-input v-model="permissionsearch" placeholder="请输入内容" style="width: 15vw"></el-input>
      <el-button type="primary" icon="el-icon-search" style="margin-left: 1vh" @click="permissionSearch">搜索</el-button>
      <el-table
          ref="permissionTable"
          :data="permissionData"
          style="width: 80vw;font-size: medium; margin-top: 2vw"
          max-height="400"
          @selection-change="handlePerSelectionChange">
          <el-table-column
            type="selection"
            width="50">
          </el-table-column>
          <el-table-column
            prop="id"
            label="编号"
            width="100">
          </el-table-column>
          <el-table-column
            prop="name"
            fixed
            label="角色名"
            width="150">
          </el-table-column>
          <el-table-column
            label="用户"
            width="400">
            <el-table-column
              prop="user_add"
              label="增加"
              width="100">
            </el-table-column>
            <el-table-column
              prop="user_update"
              label="修改"
              width="100">
            </el-table-column>
            <el-table-column
              prop="user_delete"
              label="删除"
              width="100">
            </el-table-column>
            <el-table-column
              prop="user_search"
              label="查看"
              width="100">
            </el-table-column>
          </el-table-column>
          <el-table-column
            label="角色"
            width="400">
            <el-table-column
              prop="role_add"
              label="增加"
              width="100">
            </el-table-column>
            <el-table-column
              prop="role_update"
              label="修改"
              width="100">
            </el-table-column>
            <el-table-column
              prop="role_delete"
              label="删除"
              width="100">
            </el-table-column>
            <el-table-column
              prop="role_search"
              label="查看"
              width="100">
            </el-table-column>
          </el-table-column>
          <el-table-column
            label="操作"
            width="100">
            <template slot-scope="perscope">
              <el-button
                @click.native.prevent="roleDeleteRow(perscope.$index, permissionData)"
                type="text"
                style="color: red"
                size="small">
                移除
              </el-button>
              <el-button
                @click.native.prevent="perEditRow(perscope.$index, permissionData)"
                type="text"
                size="small">
                编辑
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-button type="primary" @click="toggleRoleSelection()" style="margin-top: 2vh">取消选择</el-button>
        <el-button type="primary" @click="patchRoleDelete()" style="margin-top: 2vh">批量删除</el-button>
        </div>
      <el-result icon="error" title="暂无权限" subTitle="您无权查看角色与权限信息" v-show="!roleTableShow">
    </el-result>
    </el-tab-pane>
     <el-tab-pane label="角色添加" name="fourth">
      <el-form :model="roleForm" label-width="100px">
        <el-form-item label="角色名称">
          <el-input v-model="roleForm.name"></el-input>
        </el-form-item>
        <el-form-item label="用户添加权限">
          <el-radio-group v-model="roleForm.useradd">
            <el-radio label="是"></el-radio>
            <el-radio label="否"></el-radio>
          </el-radio-group>
        </el-form-item>
          <el-form-item label="用户修改权限">
          <el-radio-group v-model="roleForm.userupdate">
            <el-radio label="是"></el-radio>
            <el-radio label="否"></el-radio>
          </el-radio-group>
        </el-form-item>
          <el-form-item label="用户删除权限">
          <el-radio-group v-model="roleForm.userdelete">
            <el-radio label="是"></el-radio>
            <el-radio label="否"></el-radio>
          </el-radio-group>
        </el-form-item>
          <el-form-item label="用户查看权限">
          <el-radio-group v-model="roleForm.usersearch">
            <el-radio label="是"></el-radio>
            <el-radio label="否"></el-radio>
          </el-radio-group>
        </el-form-item>
          <el-form-item label="角色添加权限">
          <el-radio-group v-model="roleForm.roleadd">
            <el-radio label="是"></el-radio>
            <el-radio label="否"></el-radio>
          </el-radio-group>
        </el-form-item>
          <el-form-item label="角色修改权限">
          <el-radio-group v-model="roleForm.roleupdate">
            <el-radio label="是"></el-radio>
            <el-radio label="否"></el-radio>
          </el-radio-group>
        </el-form-item>
          <el-form-item label="角色删除权限">
          <el-radio-group v-model="roleForm.roledelete">
            <el-radio label="是"></el-radio>
            <el-radio label="否"></el-radio>
          </el-radio-group>
          </el-form-item>
          <el-form-item label="角色查看权限">
          <el-radio-group v-model="roleForm.rolesearch">
            <el-radio label="是"></el-radio>
            <el-radio label="否"></el-radio>
          </el-radio-group>
          </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onRoleSubmit" style="margin-top: 3vh">添加角色</el-button>
          <el-button style="margin-top: 3vh" @click="roleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-tab-pane>
  </el-tabs>
  <el-drawer
    title="角色与权限修改"
    :before-close="handleClose"
    :visible.sync="visible"
    direction="ltr"
    custom-class="demo-drawer"
    ref="drawer"
    >
    <div style="margin-left: 2vw; width: 25vw;">
      <el-form :model="editForm">
        <el-form-item label="角色名" :label-width="150">
          <el-input v-model="editForm.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="用户添加权限">
          <el-radio-group v-model="editForm.user_add">
            <el-radio label="是"></el-radio>
            <el-radio label="否"></el-radio>
          </el-radio-group>
        </el-form-item>
          <el-form-item label="用户修改权限">
          <el-radio-group v-model="editForm.user_update">
            <el-radio label="是"></el-radio>
            <el-radio label="否"></el-radio>
          </el-radio-group>
        </el-form-item>
          <el-form-item label="用户删除权限">
          <el-radio-group v-model="editForm.user_delete">
            <el-radio label="是"></el-radio>
            <el-radio label="否"></el-radio>
          </el-radio-group>
        </el-form-item>
          <el-form-item label="用户查看权限">
          <el-radio-group v-model="editForm.user_search">
            <el-radio label="是"></el-radio>
            <el-radio label="否"></el-radio>
          </el-radio-group>
        </el-form-item>
          <el-form-item label="角色添加权限">
          <el-radio-group v-model="editForm.role_add">
            <el-radio label="是"></el-radio>
            <el-radio label="否"></el-radio>
          </el-radio-group>
        </el-form-item>
          <el-form-item label="角色修改权限">
          <el-radio-group v-model="editForm.role_update">
            <el-radio label="是"></el-radio>
            <el-radio label="否"></el-radio>
          </el-radio-group>
        </el-form-item>
          <el-form-item label="角色删除权限">
          <el-radio-group v-model="editForm.role_delete">
            <el-radio label="是"></el-radio>
            <el-radio label="否"></el-radio>
          </el-radio-group>
          </el-form-item>
          <el-form-item label="角色查看权限">
          <el-radio-group v-model="editForm.role_search">
            <el-radio label="是"></el-radio>
            <el-radio label="否"></el-radio>
          </el-radio-group>
          </el-form-item>
      </el-form>
      <div>
        <el-button @click="cancelForm">取 消</el-button>
        <el-button type="primary" @click="closeDrawer()">确 定</el-button>
      </div>
    </div>
  </el-drawer>
</div>
</template>

<script>
import {save_log} from "@/components/utils.js";

export default {
  name: "InfoManage",
  mounted(){
    this.$http.get("http://59.77.17.71:5001/getuser").then(res=>{
      console.log(res)
      if(res.data === "no_permission"){
        this.userTableShow = false
      }else{
        this.originalData = res.data
        this.tableData = this.originalData
      }
    })
    // this.$http.get("http://59.77.17.71:5001/getrole").then(res=>{
    //   console.log(res.data)
    //   this.realRoleList = res.data["list"]
    //   this.roleList = ["全部"].concat(res.data["list"])
    //   let roleData = []
    //   let i = 1
    //   let option = []
    //   res.data["table"].forEach(role =>{
    //     console.log(role)
    //     let r = {
    //       id: i,
    //       name: role.name,
    //       real_id: role["real_id"]
    //     }
    //     i += 1
    //     roleData.push(r)
    //     option.push(this.$createElement('option', null, role.name))
    //   })
    //   this.roleData = roleData
    //   this.originalRoleData = this.roleData
    //   this.option = option
    // })
    this.$http.get("http://59.77.17.71:5001/getpermission").then(res=>{
      console.log(res.data)
      if(res.data === "no_permission"){
        this.roleTableShow = false
      }else{
        this.permissionData = res.data
        this.originalPerData = res.data
      }
      let j = 1
      let roleList = []
      let option = []
      res.data.forEach(per=>{
        per["id"] = j
        roleList.push(per.name)
        j += 1
        option.push(this.$createElement('option', null, per.name))
      })
      this.realRoleList = roleList
      this.roleList = ["全部"].concat(roleList)
      this.option = option
    })
  },
  methods: {
    deleteRow(index, rows) {
      if(rows[index].name === "admin"){
        this.$message.error("不能删除超级管理员！")
        save_log("尝试删除超级管理员，被系统阻止。")
      }else{
        let id = [this.originalData[index]["real_id"]]
        this.$http.post("http://59.77.17.71:5001/deleteuser", {id: id}).then(res=>{
          if(res.data === "success"){
            rows.splice(index, 1);
            this.originalData = this.tableData
            save_log("删除用户" + this.originalData[index].name)
          }else{
            this.$message.error("删除失败！")
            save_log("尝试删除用户" + this.originalData[index].name, + "，删除失败。")
          }
        })
      }
    },
    selectChange(){
      this.search()
    },
    disableRow(index, rows){
      if(rows[index].name === "admin"){
        this.$message.error("不能禁用超级管理员！")
        save_log("尝试禁用超级管理员，被系统阻止。")
      }
      let state = rows[index].state === "启用"? "禁用": "启用"
      console.log(rows[index]["real_id"])
      this.$http.post("http://59.77.17.71:5001/updateuser", {id: rows[index]["real_id"], name: rows[index].name,
        role: rows[index].role, state: state}).then(res=>{
        if(res.data === "no_permission"){
          this.$message.error("您没有该权限！")
          save_log("尝试禁用用户" + rows[index].name + "但没有权限")
        }
        else if(res.data === "success"){
          rows[index].state = state
          this.originalData = this.tableData
          console.log("禁用" + rows[index].name)
          save_log("禁用用户" + rows[index].name)
        }else{
          this.$message.error("修改失败！")
          save_log("尝试禁用用户" + rows[index].name + "但操作失败")
        }
      })
    },
    onEditUser(){
      this.editUser = document.getElementById("editUser").value
      console.log(this.editUser)
    },
    onEditRole(){
      this.editRole = document.getElementById("editRole").value
      console.log(this.editRole)
    },
    editRow(index, rows){
      if(rows[index].name === "admin"){
        this.$message.error("不能编辑超级管理员！")
        save_log("尝试编辑超级管理员被系统阻止")
        return
      }
      let _this = this
      console.log(index, rows)
      this.editRole = this.tableData[index].role
      this.editUser = this.tableData[index].name
      const h = this.$createElement;
      this.$msgbox({
          title: '消息',
          message:
          h('div', null, [
              h('p', null, [
                h('span', null, '用户名 '),
                  h('input', { attrs: {
                    id:'editUser'
                  },
                  domProps: {
                      value: _this.editUser,
                  },
                  on: { change: _this.onEditUser },
                  style: 'margin-left: 1vh' }, _this.tableData[index].name)
              ]),
              h('p', { style: 'margin-top: 1vh' }, [
              h('span', null, '角色'),
              h('select', { attrs: {
                    id:'editRole'
                },
                domProps: {
                    value: _this.editRole,
                },
                on: { change: _this.onEditRole },
                style: 'margin-left: 1vh' }, this.option)
            ]),
          ]),
          showCancelButton: true,
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          beforeClose: (action, instance, done) => {
            let name = this.editUser
            let role = this.editRole
            this.$http.post("http://59.77.17.71:5001/updateuser", {id: rows[index]["real_id"], name: name,
              role: role, state: rows[index].state}).then(res=>{
              if(res.data === "no_permission"){
                this.$message.error("您没有该权限！")
                save_log("尝试编辑用户" + rows[index].name + "但没有权限")
              }
              else if(res.data === "success"){
                this.tableData[index].name = this.editUser
                this.tableData[index].role = this.editRole
                this.originalData = this.tableData
                done();
                save_log("编辑用户" + rows[index].name)
              }else{
                this.$message.error("修改失败！")
                save_log("尝试编辑用户" + rows[index].name + "但操作失败")
                done();
              }
            })

          }
        })
    },
    toggleSelection(rows) {
        if (rows) {
          rows.forEach(row => {
            this.$refs.multipleTable.toggleRowSelection(row);
          });
        } else {
          this.$refs.multipleTable.clearSelection();
        }
    },
    handleSelectionChange(val) {
      this.multiSelection = val;
      console.log(this.multiSelection)
    },
    handleRoleSelectionChange(val){
      this.roleMultiSelection = val;
    },
    handlePerSelectionChange(val){
      this.roleMultiSelection = val
    },
    patchDelete(){
      let deleteList = []
      this.multiSelection.forEach(info=>{
        if(info.name !== "admin"){
          deleteList.push(info.name)
        }else{
          this.$message.error("不能删除超级管理员！")
          save_log("尝试删除超级管理员被系统阻止")
        }
      })
      let indexList = []
      let idList = []
      for(let i = 0; i < this.tableData.length; i++){
        let user = this.tableData[i]
        if(deleteList.indexOf(user.name)>=0){
          indexList.push(i)
          idList.push(user["real_id"])
        }
      }
      this.$http.post("http://59.77.17.71:5001/deleteuser", {id: idList}).then(res=>{
        if(res.data === "no_permission"){
          this.$message.error("您没有该权限！")
          save_log("尝试删除用户" + deleteList.join("、") + "但没有权限")
        }
        else if(res.data === "success"){
          indexList.sort().reverse()
          indexList.forEach(index=>{
            this.tableData.splice(index, 1)
          })
          this.originalData = this.tableData
          save_log("删除用户" + deleteList.join("、"))
        }else{
          this.$message.error("删除失败！")
          save_log("尝试删除" + deleteList.join("、") + "但操作失败")
        }
      })
    },
    onSubmit(){
      let flag = 0
      for(let i = 0; i < this.tableData.length; i++){
        if(this.tableData[i].name === this.form.name){
          this.$message.error("用户名已存在！")
          this.reset()
          flag = 1
          save_log("尝试添加用户" + this.form.name + "但用户名已存在")
          break
        }
      }
      if(!flag){
        this.$http.post("http://59.77.17.71:5001/adduser", {name: this.form.name, password: this.form.password,
        role: this.form.role, state: this.form.state}).then(res=>{
        if(res.data["state"] === "no_permission"){
          this.$message.error("您没有权限！")
          save_log("尝试添加用户" + this.form.name + "但没有权限")
        }
        else if(res.data["state"] === "exist"){
          this.$message.warning("用户名已存在！")
        }
        else if(res.data["state"] === "success"){
          save_log("添加用户" + this.form.name)
          let id = this.tableData[this.tableData.length-1].id + 1
          let user = {
            id: id,
            real_id: res.data["id"],
            name: this.form.name,
            role: this.form.role,
            state: this.form.state
          }
          this.tableData.push(user)
          this.originalData = this.tableData
          this.reset()
          this.$message.success("添加成功！")
        }else{
          this.$message.error("添加失败！")
          save_log("尝试添加用户" + this.form.name + "但操作失败")
        }
      })
      }
    },
    reset(){
      this.form.name = ''
      this.form.role = '普通用户'
      this.form.state = '启用'
    },
    search(){
      // let roleList = this.roleList.slice()
      // roleList.shift()
      let roles = this.realRoleList.indexOf(this.value) >=0? [this.value] : this.realRoleList
      let userList = []
      console.log(roles)
      this.originalData.forEach(user=>{
        console.log(user.role)
        if(user.name.indexOf(this.input)>=0 && roles.indexOf(user.role) >= 0){
          userList.push(user)
        }
      })
      this.tableData = userList;
    },
    onRoleSubmit(){
      let flag = 0
      this.realRoleList.forEach(role=>{
        if(this.roleForm.name === role){
          this.$message.error("角色名已存在！")
          save_log("尝试添加角色" + this.roleForm.name + "但角色名已存在")
          this.roleReset()
          flag = 1
        }
      })
      if(!flag){
        let f = this.roleForm
        this.$http.post("http://59.77.17.71:5001/addrole", {name: f.name, useradd: f.useradd, userupdate: f.userupdate,
        userdelete: f.userdelete, usersearch: f.usersearch, roleadd: f.roleadd, roleupdate: f.roleupdate, roledelete: f.roledelete,
        rolesearch: f.rolesearch}).then(res=>{
          if(res.data === "no_permission"){
            this.$message.error("您没有权限！")
            save_log("尝试添加角色" + this.roleForm.name + "但没有权限")
          }
          else if(res.data === "success"){
            this.roleList.push(this.roleForm.name)
            this.realRoleList.push(this.roleForm.name)
            // this.originalRoleData.push({
            //   id: this.roleData.length + 1,
            //   name: this.roleForm.name,
            // })
            this.permissionData.push({
              id: this.permissionData.length + 1,
              name: this.roleForm.name,
              user_add: this.roleForm.useradd,
              user_update: this.roleForm.userupdate,
              user_delete: this.roleForm.userdelete,
              user_search: this.roleForm.usersearch,
              role_add: this.roleForm.roleadd,
              role_update: this.roleForm.roleupdate,
              role_delete: this.roleForm.roledelete,
              role_search: this.roleForm.rolesearch,
              per_add: this.roleForm.peradd,
              per_update: this.roleForm.perupdate,
              per_delete: this.roleForm.perdelete,
              per_search: this.roleForm.persearch,
            })
            this.permissionData = this.originalPerData
            this.option.push(this.$createElement('option', null, this.roleForm.name))
            this.roleReset()
            this.$message.success("添加成功！")
            save_log("添加角色" + this.roleForm.name)
          }else{
            this.$message.error("添加失败！")
            save_log("尝试添加角色" + this.roleForm.name + "但操作失败")
          }
        })
      }
    },
    roleReset(){
      this.roleForm.name = ''
    },
    roleEditRow(index, rows){
      if(rows[index].name === "超级管理员"){
        this.$message.error("不能编辑超级管理员！")
        save_log("尝试编辑超级管理员但被系统阻止")
        return
      }
      this.$prompt('角色名', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
      }).then(({ value }) => {
        this.$http.post("http://59.77.17.71:5001/updaterole", {name: value, id: rows[index]["real_id"]}).then(res=>{
          if(res.data === "no_permission"){
            this.$message.error("您没有该权限！")
            save_log("尝试编辑角色" + rows[index].name + "但没有权限")
          }
          else if(res.data === "success"){
            save_log("编辑角色" + rows[index].name)
            for(let i = 0; i < this.roleList.length; i++){
              if(this.roleList[i] === rows[index].name){
                this.roleList[i] = value
                this.realRoleList[i-1] = value
                break
              }
            }
            this.tableData.forEach(user=>{
              if(user.role === rows[index].name){
                user.role = value
              }
            })
            this.option.forEach(op=>{
              console.log(op.children[0].text)
              if(op.children[0].text === rows[index].name){
                op.children[0].text = value
              }
            })
            this.originalRoleData.forEach(role=>{
              if(role.name === rows[index].name){
                role.name = value
              }
            })
            rows[index].name = value
          }else{
            this.$message.error("修改失败！")
            save_log("尝试编辑角色" + rows[index].name + "但操作失败")
          }
        })
      })
    },
    onDeleteRole(){
      this.updateRole = document.getElementById("updateRole").value
    },
    deleteRole(role, new_role){
      this.$http.post("http://59.77.17.71:5001/deleterole", {id: [role["real_id"]], role: this.updateRole}).then(res=>{
      if(res.data === "no_permission"){
        this.$message.error("您没有权限！")
        save_log("尝试删除角色" + role.name + "但没有权限")
      }
      else if(res.data === "success") {
        save_log("删除角色" + role.name)
        this.tableData.forEach(user=>{
          if(user.role === role.name){
            user.role = new_role
          }
        })
        this.originalData = this.tableData
        for (let i = 0; i < this.roleList.length; i++) {
          if (this.roleList[i] === role.name) {
            this.roleList.splice(i, 1)
            this.originalPerData.splice(i - 1, 1)
            this.realRoleList.splice(i - 1, 1)
            this.option.splice(i - 1, 1)
            break
          }
        }
        for(let i = 0; i < this.permissionData.length; i++){
          if(this.permissionData[i].name === role.name){
            this.permissionData.splice(i, 1)
            break
          }
        }
      }else{
        this.$message.error("删除失败！")
        save_log("尝试删除角色" + role.name + "但操作失败")
      }
      })
    },
    roleDeleteRow(index, rows){
      let name = rows[index].name
      let flag = 0
      this.tableData.forEach(user =>{
        if(user.role === name){
          flag = 1
          let _this = this
          let h = this.$createElement
          let option = this.option.slice()
          for(let i = 0; i < option.length; i++){
            if(option[i].children[0].text === name){
                option.splice(i, 1)
              }
          }
          this.$msgbox({
          title: '请选择删除角色对应用户需要修改为的角色',
          message:
          h('div', null, [
              h('p', { style: 'margin-top: 1vh' }, [
              h('span', null, '角色'),
              h('select', { attrs: {
                    id:'updateRole'
                },
                domProps: {
                    value: _this.updateRole,
                },
                on: { change: _this.onDeleteRole },
                style: 'margin-left: 1vh' }, option)
            ]),
          ]),
          showCancelButton: true,
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          beforeClose: (action, instance, done) => {
            if(this.updateRole === ''){
              this.$message.warning("请选择修改后的角色！")
            }else{
              this.deleteRole(rows[index], this.updateRole)
              _this.updateRole = ''
            }
            done()
          }
        })
        }
      })
      if(!flag){
        this.deleteRole(rows[index], this.updateRole)
      }
    },
    onDeleteMultiRole(){
      this.updateMultiRole = document.getElementById("updateMultiRole").value
    },
    patchRoleDelete(){
      let flag = 0
      for(let i = 0; i < this.roleMultiSelection.length; i++){
        for(let j = 0; j < this.tableData.length; j++){
          if(this.tableData[j].role === this.roleMultiSelection[i].name){
            flag = 1
            break
          }
        }
        if(flag === 1){
          break
        }
      }
      if(flag === 1){
        let option = this.option.slice()
        this.roleMultiSelection.forEach(role =>{
          for(let i = 0; i < option.length; i++){
            if(option[i].children[0].text === role.name){
                option.splice(i, 1)
              }
          }
        })
        let _this = this
        let h = this.$createElement
        this.$msgbox({
          title: '请选择删除角色对应用户需要修改为的角色',
          message:
          h('div', null, [
              h('p', null, '注意：所有角色对应的用户将修改为相同角色'),
              h('p', { style: 'margin-top: 1vh' }, [
              h('span', null, '角色'),
              h('select', { attrs: {
                    id:'updateMultiRole'
                },
                domProps: {
                    value: _this.updateMultiRole,
                },
                on: { change: _this.onDeleteMultiRole },
                style: 'margin-left: 1vh' }, option)
            ]),
          ]),
          showCancelButton: true,
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          beforeClose: (action, instance, done) => {
            console.log(this.updateMultiRole)
            console.log(this.roleMultiSelection)
            if(this.updateMultiRole === ''){
              this.$message.warning("请选择修改后的角色！")
            }else{
              this.roleMultiSelection.forEach(role=>{
                console.log(role)
                this.deleteRole(role, this.updateMultiRole)
              })
              _this.updateMultiRole = ''
            }
            done()
          }
        })
      }else{
        this.roleMultiSelection.forEach(role=>{
          this.deleteRole(role, this.updateMultiRole)
        })
        this.updateMultiRole = ''
      }
    },
    toggleRoleSelection(rows){
        if (rows) {
          rows.forEach(row => {
            this.$refs.roleTable.toggleRowSelection(row);
          });
        } else {
          this.$refs.roleTable.clearSelection();
        }
    },
    roleSearch(){
      let l = []
      console.log(this.originalRoleData)
      this.originalRoleData.forEach(role =>{
        if(role.name.indexOf(this.rolesearch) >= 0){
          l.push(role)
        }
      })
      this.roleData = l
    },
    permissionSearch(){
      let l = []
      this.originalPerData.forEach(per =>{
        if(per.name.indexOf(this.permissionsearch) >= 0){
          l.push(per)
        }
      })
      this.permissionData = l
    },
    perEditRow(index, rows){
      let role = rows[index]
      let params = ["name", "user_add", "user_update", "user_delete", "user_search", "role_add", "role_update", "role_delete", "role_search", "real_id"]
      params.forEach(param=>{
        this.editForm[param] = role[param]
      })
      this.editForm.original_name = role.name
      this.editForm.index = index
      this.visible = true
    },
    closeDrawer(){
      let flag = 0
      this.originalPerData.forEach(per=>{
        if(per.name === this.editForm.name && this.editForm.original_name !== per.name){
          this.$message.error("角色名已存在！")
          flag = 1
        }
      })
      if(!flag){
        let f = this.editForm
      this.$http.post("http://59.77.17.71:5001/updatepermission", {name: f.name, id: f.real_id, useradd: f.user_add, userupdate: f.user_update,
        userdelete: f.user_delete, usersearch: f.user_search, roleadd: f.role_add, roleupdate: f.role_update, roledelete: f.role_delete,
        rolesearch: f.role_search
      }).then(res=>{
          if(res.data === "no_permission"){
            save_log("尝试修改角色" + f.name + "权限，但没有权限")
            this.$message.error("您没有该权限！")
          }
          else if(res.data === "success"){
            save_log("修改角色" + f.name + "权限")
            for(let i = 0; i < this.roleList.length; i++){
              if(this.roleList[i] === f.original_name){
                this.roleList[i] = f.name
                this.realRoleList[i-1] = f.name
                break
              }
            }
            this.tableData.forEach(user=>{
              if(user.role === f.original_name){
                user.role = f.name
              }
            })
            this.option.forEach(op=>{
              console.log(op.children[0].text)
              if(op.children[0].text === f.original_name){
                op.children[0].text = f.name
              }
            })
            this.originalPerData.forEach(role=>{
              if(role.name === f.original_name){
                role.name = f.name
              }
            })
            // this.roleData[f.index].name = f.name
            let params = ["name", "user_add", "user_update", "user_delete", "user_search", "role_add", "role_update", "role_delete", "role_search", "real_id"]
            params.forEach(param=>{
              this.permissionData[f.index][param] = f[param]
            })
            this.visible = false
          }else{
            this.$message.error("修改失败！")
            save_log("尝试修改角色" + f.name + "权限，但操作失败")
          }
      })
      }
    },
  },
  data() {
    return {
      tableData: [],
      originalData: [],
      roleList: [],
      realRoleList: [],
      roleData: [],
      originalRoleData: [],
      permissionData: [],
      originalPerData: [],
      editUser: '',
      editRole: '',
      multiSelection: [],
      roleMultiSelection: [],
      perMultiSelection: [],
      input: '',
      value: '',
      activeName: 'first',
      form: {
        name: '',
        password: '123456',
        role: '普通用户',
        state: '启用'
      },
      roleForm: {
        name: '',
        useradd: '否',
        userupdate: '否',
        userdelete: '否',
        usersearch: '否',
        roleadd: '否',
        roleupdate: '否',
        roledelete: '否',
        rolesearch: '否',
        peradd: '否',
        perupdate: '否',
        perdelete: '否',
        persearch: '否'
      },
      option: [],
      updateRole: '',
      updateMultiRole: '',
      rolesearch: '',
      permissionsearch: '',
      visible: false,
      editForm: {
        name: '',
        user_add: '',
        user_update: '',
        user_delete: '',
        user_search: '',
        role_add: '',
        role_update: '',
        role_delete: '',
        role_search: '',
        real_id: '',
        original_name: '',
        index: 0
      },
      userTableShow: true,
      roleTableShow: true
    }
  }
}
</script>

<style scoped>
.title{
    text-align: center;
    padding-top: 3.5vh;
    padding-bottom: 3.5vh;
    color: black;
    font-size: 4vh;
    width: 60vw;
    margin-left: 20vw;
    /*border-radius: 0px 0px 50px 50px;*/
    /*background-color: lightgray;*/
    /*margin-bottom: 5vh;*/
}
.demo-drawer__footer{
  position: fixed;
  bottom: 2vh;
  margin-left: 5%;
  width: 90%;
}
</style>