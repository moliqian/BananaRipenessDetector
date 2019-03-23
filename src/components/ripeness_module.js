import React, { Component } from 'react';
import axios from 'axios'

var serverURL = "http://localhost:5000/"

export default class RipenessModule extends Component {
    constructor(props){
        super()
        this.state = {

        }

        this.handle_file_input = this.handle_file_input.bind(this)
    }
    handle_file_input(e){
        console.log(e.target.files[0])
        let file = e.target.files[0]
        if(file){
            let data = new FormData()
            data.append('file', file)
            axios({
                method: 'post',
                url: serverURL + "upload",
                data: data
              }).then(function(response) {
                  console.log("response!")
                //response.data.pipe(fs.createWriteStream('ada_lovelace.jpg'))
              });
        }
    }
    render() {
        return (
        <div className="App">
            <form>
                <h3>Import your image!</h3>
                <input type="file" onChange={this.handle_file_input}/>
            </form>
            <img style={{width: '300px'}} src="http://localhost:5000/banana"></img>
        </div>
        );
    }
}


