import React, { Component } from 'react';
import axios from 'axios'

var serverURL = "http://gv79.pythonanywhere.com/"

const introStyle = {
    fontFamily: 'Karla',

    fontSize: '1.2em'
};

const divStyle = {
    margin: '20px 28% 25px 28%',
    paddingTop: '20px',
    borderTop: '1px solid #c6c6c6'
}

const flexStyle = {
    display: 'flex',
    flex: '1',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center'
}

const formStyle = {
    textAlign: 'center',
    width: '15em',
    fontSize: '1.2em',
    margin: '1em'
}

const hrLine = {
    borderTop: '1px solid #c6c6c6',
    height: '5px',
    margin: '15px 20% 0 20%'
}

const nameStyle = {
    margin: '5px',
    fontSize: '1.2em'
}

const iconStyle = {
    margin: '2px',
    fontSize: '2em'
}

const aS = {
    textDecoration: 'none',
    color: 'black'
}

export default class RipenessModule extends Component {
    constructor(props){
        super()
        this.state = {
            original_url: "http://gv79.pythonanywhere.com/banana?",
            url: "http://gv79.pythonanywhere.com/banana?",
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
        <div style={divStyle}><p style={introStyle}>This web application computes the ripeness of a banana in an image. Upload your image below to test the algorithm out! In order to reduce computation times, upload photos with lower resolution.</p></div>
            {this.state.loading ? (
                <img src={require('../loading.gif')}/ >
            ) : 
                <img style={{width: '800px', height: '500px', 'objectFit': 'contain'}} src={this.state.url}/ >
            }
            <form className="md-form">
                <div style={flexStyle}>
                    <div>{this.state.x}</div>
                    <input type="file" className="form-control-file" style={formStyle} id="exampleFormControlFile1" onChange={this.handle_file_input}/>
                </div>
            </form>
            <div style={hrLine}></div>
            <div style={flexStyle}>
                 <div style={nameStyle}><a style={aS} href="https://giavinhlam.me" target="_blank">Giavinh Lam</a> - <a style={aS} href="http://www.petarkenic.host/" target="_blank">Petar Kenic</a> - <a style={aS}>Greg Hetherington</a></div>
                 <div style={iconStyle}><a style={aS} href="https://github.com/peken97/BananaRipenessDetector" target="_blank"><i className="fab fa-github"></i></a> <a style={aS} href="https://github.com/peken97/BananaRipenessDetector/blob/master/CIS%204720%20FINAL%20REPORT%20-%20IMAGE.pdf" target="_blank"><i className="fas fa-info-circle"></i></a></div>
            </div>
        </div>
        );
    }
}


