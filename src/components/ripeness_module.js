import React, { Component } from 'react';
import axios from 'axios'

var serverURL = "http://localhost:5000/"

export default class RipenessModule extends Component {
    constructor(props){
        super()
        this.state = {
            original_url: "http://localhost:5000/banana?",
            url: "http://localhost:5000/banana?",
            index: 0,
            loading: false
        }

        this.handle_file_input = this.handle_file_input.bind(this)
    }
    handle_file_input(e){
        console.log(e.target.files[0])
        let file = e.target.files[0]
        let refresh = false;
        let referenceToThis = this;
        if (file){
            referenceToThis.setState({
              loading: true
            })
            let data = new FormData()
            data.append('file', file)
            axios({
                method: 'post',
                url: serverURL + "upload",
                data: data,
              }).then(function(response) {
                  let today = new Date()
                  let url = referenceToThis.state.url
                  url = referenceToThis.state.original_url + today.getTime()
                  referenceToThis.setState({
                    url: url,
                    loading: false
                  })
                  
                //response.data.pipe(fs.createWriteStream('ada_lovelace.jpg'))
              });
        }
        
        if(refresh == true){
            console.log("Jeez")
            this.setState({})
        }
    }
    render() {
        return (
        <div className="App">
            <form>
                <h3>Import your image!</h3>
                <input type="file" onChange={this.handle_file_input}/>
                <div>{this.state.x}</div>
            </form>
            {this.state.loading ? (
                <img src={require('../loading.gif')}/ >
            ) : 
                <img style={{width: '300px'}} src={this.state.url}/ >
            }
        </div>
        );
    }
}


