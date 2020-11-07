import React from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';

import { withStyles } from '@material-ui/core/styles';

import Button from '@material-ui/core/Button';
import AppBar from '@material-ui/core/AppBar';
import SwipeableDrawer from '@material-ui/core/SwipeableDrawer';
import Drawer from '@material-ui/core/Drawer';
import Toolbar from '@material-ui/core/Toolbar';
import List from '@material-ui/core/List';
import Typography from '@material-ui/core/Typography';
import ChevronLeftIcon from '@material-ui/icons/ChevronLeft';
import MenuIcon from '@material-ui/icons/Menu';
import IconButton from '@material-ui/core/IconButton';
import Divider from '@material-ui/core/Divider';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import InboxIcon from '@material-ui/icons/MoveToInbox';
import MailIcon from '@material-ui/icons/Mail';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';

import { FixedSizeList } from 'react-window';
import AutoSizer from "react-virtualized/dist/commonjs/AutoSizer";

const API_PATH = 'http://localhost:8123/';

const styles = {
  container: {
    width: '100%',
    margin: '0',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif',
    flexGrow: 1,
  },
  paper: {
    padding: '2em',
    margin: '12px',
    textAlign: 'center'
  },
  status: {
    padding: '2em',
    margin: '12px',
    height: '400px'
  },
  ss: {
    margin: '20px',
    width: 'calc(100% - 40px)'
  },
  pointer: {
    position: 'absolute',
    display: 'block',
    top: '0',
    left: '0',
    width: '10px',
    height: '10px',
    borderRadius: '20px',
    backgroundColor: 'red'
  }
};

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isCalling: false,
      items: {},
      ss: null,
      open: false,
      windowName: '',
      timeValue: 1,
      nameValue: '',
      x: 0,
      y: 0,
      windowPosition: {x: 0, y: 0},
      setNameValue: ''
    };
    this.handleApi = this.handleApi.bind(this);
    this.handleApiWindow = this.handleApiWindow.bind(this);
    this.handleApiSS = this.handleApiSS.bind(this);
    this.handleApiSubWindow = this.handleApiSubWindow.bind(this);
    this.handleApiSubSS = this.handleApiSubSS.bind(this);
    this.handleDrawerOpen = this.handleDrawerOpen.bind(this);
    this.handleDrawerClose = this.handleDrawerClose.bind(this);
    this.setPosition = this.setPosition.bind(this);
    this.handleChangeTime = this.handleChangeTime.bind(this);
    this.handleChangeName = this.handleChangeName.bind(this);
    this.handleChangeId = this.handleChangeId.bind(this);
    this.handleApiCreateItem = this.handleApiCreateItem.bind(this);
    this.handleApiGetItems = this.handleApiGetItems.bind(this);
    this.handleApiStartWS = this.handleApiStartWS.bind(this);
  }

  async handleApiWindow() {
    const result = await this.handleApi('get', 'window', {
      time: this.state.timeValue
    });
    result ? this.setState(state => ({ windowName: result.name })) : null
  }

  async handleApiSS() {
    const result = await this.handleApi('get', 'ss', {
      keyword: this.state.nameValue
    });
    result ? this.setState(state => ({ ss: result.img })) : null
  }

  async handleApiSubWindow() {
    const result = await this.handleApi('get', 'sub/window', {
      time: this.state.timeValue
    });
    result ? this.setState(state => ({ windowName: result.name })) : null
  }

  async handleApiSubSS() {
    const result = await this.handleApi('get', 'sub/ss', {
      keyword: this.state.nameValue
    });
    result ? this.setState(state => ({ ss: result.img })) : null
  }

  async handleApiGetItems() {
    const result = await this.handleApi('get', 'item');
    result ? this.setState(state => ({ items: result.item })) : null
  }

  async handleApiStartWS() {
    const result = await this.handleApi('get', 'ws');
  }

  async handleApiCreateItem() {
    const result = await this.handleApi('post', 'item', {
      name: this.state.setNameValue,
      x: this.state.x,
      y: this.state.y,
      window: this.state.windowName
    })
    result ? console.log(result) : null
  }

  async handleApi(method='get', path='', body=null) {
    if (this.state.isCalling) return
    if (!['get', 'post'].find(e => e == method)) return

    console.log("call API...", method, API_PATH+path, body);
    this.setState(state => ({ isCalling: true }));
    let result;
    try {
      if (method == 'get') {
        if(!!body) {
          result = await axios.get(API_PATH + path, {params: body});
        } else {
          result = await axios.get(API_PATH + path);
        }
      } else if (method == 'post') {
        result = await axios.post(API_PATH + path, body);
      }
      if (result.status == 200) {
        return result.data
      }
    } catch (e) {
      console.error(e);
      return false
    } finally {
      this.setState(state => ({ isCalling: false }));
      console.log("API results", result);
    }
  }

  handleChangeTime(e) {
    let time = 0;
    const value = e.target.value;
    if (isNaN(value)) return
    time = value < 0 ? 0 : value > 20 ? 20 : value
    this.setState(state => ({ timeValue: time }));
  }

  handleChangeName(e) {
    const name = e.target.value;
    this.setState(state => ({ nameValue: name }));
  }

  handleChangeId(e) {
    const value = e.target.value;
    if (!value.match(/^[A-Za-z0-9]*$/)) return
    this.setState(state => ({ setNameValue: value }));
  }

  setPosition(e) {
    if (!e.target) return
    const rect = e.target.getBoundingClientRect();
    const mag = e.target.naturalWidth / rect.width;
    let x = e.pageX - (rect.x + window.pageXOffset);
    let y = e.pageY - (rect.y + window.pageYOffset);
    this.setState(state => ({ x: e.pageX, y: e.pageY }))
    x *= mag
    y *= mag
    x = Math.round(x * 10) / 10
    y = Math.round(y * 10) / 10
    this.setState(state => ({ windowPosition: {x: x, y: y} }))
  }

  handleDrawerOpen() {
    this.setState(state => ({ open: true }));
  };

  handleDrawerClose() {
    this.setState(state => ({ open: false }));
  };

  render() { return (
    <>
      <AppBar position="static">
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            onClick={this.handleDrawerOpen}
            edge="start"
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6">
            python で自動化プログラム
          </Typography>
          <Button color="inherit">Connect (未実装)</Button>
        </Toolbar>
      </AppBar>

      <SwipeableDrawer
        anchor="left"
        open={this.state.open}
        onClose={this.handleDrawerClose}
        onOpen={this.handleDrawerOpen}
      >
        <Divider />
        <List>
          {['Inbox', 'Starred', 'Send email', 'Drafts'].map((text, index) => (
            <ListItem button key={text}>
              <ListItemIcon>{index % 2 === 0 ? <InboxIcon /> : <MailIcon />}</ListItemIcon>
              <ListItemText primary={text} />
            </ListItem>
          ))}
        </List>
        <Divider />
        <List>
          {['All mail', 'Trash', 'Spam'].map((text, index) => (
            <ListItem button key={text}>
              <ListItemIcon>{index % 2 === 0 ? <InboxIcon /> : <MailIcon />}</ListItemIcon>
              <ListItemText primary={text} />
            </ListItem>
          ))}
        </List>
      </SwipeableDrawer>

      <Grid container>
        { this.state.windowName ? (<Grid item xs={12}>
          <Paper className={this.props.classes.paper}>
            <p>window name: </p>
            <span>{this.state.windowName}</span>
          </Paper>
        </Grid>) : null}
        <Grid item xs={6}>
          <Paper className={this.props.classes.paper}>
            <Button color="primary" onClick={this.handleApiWindow}>get Window</Button><br/>
            <Button color="primary" onClick={this.handleApiSubWindow}>get sub Window</Button><br/>
            <input type="text" value={this.state.timeValue} onChange={this.handleChangeTime} /> sec
          </Paper>
        </Grid>
        <Grid item xs={6}>
          <Paper className={this.props.classes.paper}>
            <Button color="primary" onClick={this.handleApiSS}>get SS</Button><br/>
            <Button color="primary" onClick={this.handleApiSubSS}>get sub SS</Button><br/>
            window名: <input type="text" value={this.state.nameValue} onChange={this.handleChangeName} />
          </Paper>
        </Grid>
        <Grid item xs={12}>
          <Paper className={this.props.classes.paper}>
            <Button color="primary" onClick={this.handleApiCreateItem} disabled={!this.state.windowName || !this.state.windowPosition.x || !this.state.setNameValue}>
              put Position
            </Button><br/>
            名前(英数) <input type="text" value={this.state.setNameValue} onChange={this.handleChangeId} /><br/>
            window名: <span>{this.state.windowName}</span><br/>
            相対位置: <span>{this.state.windowPosition.x + '  ' + this.state.windowPosition.y}</span>
          </Paper>
        </Grid>
        { false ? <Grid item xs={12}>
          <Paper className={this.props.classes.status}>
            <AutoSizer>
              {({ height, width }) => (
                <FixedSizeList height={height} width={width} itemSize={46} itemCount={200}>
                  {renderRow}
                </FixedSizeList>
              )}
            </AutoSizer>
          </Paper>
        </Grid> : null}
        <Grid item xs={12}>
          {this.state.ss ? (
            <>
              <img src={"data:image/jpeg;base64," + this.state.ss} className={this.props.classes.ss} onClick={this.setPosition} />
              <span className={this.props.classes.pointer} style={{top: this.state.y -5, left: this.state.x -5}}></span>
            </>
            ): null}
        </Grid>
        <Grid item xs={6}>
          <Paper className={this.props.classes.paper}>
            <Button color="primary" onClick={this.handleApiGetItems}>
              get Items
            </Button><br/>
          </Paper>
        </Grid>
        <Grid item xs={6}>
          <Paper className={this.props.classes.paper}>
            <Button color="primary" onClick={this.handleApiStartWS}>
              start Websocket
            </Button><br/>
          </Paper>
        </Grid>
      </Grid>
    </>
  )}
}

function renderRow(props) {
  const { index, style } = props;

  return (
    <ListItem button style={style} key={index}>
      <ListItemText primary={`Item ${index + 1}`} />
    </ListItem>
  );
}
renderRow.propTypes = {
  index: PropTypes.number.isRequired,
  style: PropTypes.object.isRequired,
};

export default withStyles(styles)(App);
