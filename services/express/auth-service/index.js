'use strict'

// Import required modules
require('dotenv').config()
const express = require('express');
const mongoose = require('mongoose');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const morgan = require('morgan');
const zxcvbn = require('zxcvbn');

// Connect to MongoDB
mongoose.connect(process.env.MONGODB_PATH);

// Define User schema
const UserSchema = new mongoose.Schema({
  username: {
    type: String,
    required: true,
  },
  password: {
    type: String,
    required: true,
    minLength: 8,
    maxLength: 64,
  },
  email: {
    type: String,
    required: true,
    match: [/^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/, 'Please fill a valid email address'],
  },
});

// Pre-save hook to hash password
UserSchema.pre('save', async function(next) {
  if (this.isModified('password')) {
    this.password = await bcrypt.hash(this.password, Number(process.env.SALT_ROUNDS));
  }
  next();
});

// Method to check password validity
UserSchema.methods.isValidPassword = function(password) {
  return bcrypt.compare(password, this.password);
};

// Create User model
const User = mongoose.model('User', UserSchema);

// Initialize Express app
const app = express();
app.use(express.json());
app.use(morgan(process.env.MORGAN_MODE));

// Register route
app.post('/register', async (req, res) => {
  const passwordStrength = zxcvbn(req.body.password);
  if (passwordStrength.score < 3) {
    return res.status(400).json({
      message: 'Password is too weak',
      suggestions: passwordStrength.feedback.suggestions,
    });
  }
  
  const user = new User(req.body);
  try {
    await user.save();
    res.sendStatus(201); 
  } catch (error) {
    res.status(400).send(error.message)
  }
});

// Login route
app.post('/login', async (req, res) => {
  const user = await User.findOne({ username: req.body.username });
  if (!user || !(await user.isValidPassword(req.body.password))) {
    return res.sendStatus(401);
  }
  const token = jwt.sign({ _id: user._id }, process.env.SECRET_KEY);
  res.send({ token });
});

// Secured route
app.get('/secured', async (req, res) => {
  const authHeader = req.headers.authorization;
  if (!authHeader) {
    return res.sendStatus(401);
  }
  const token = authHeader.split(' ')[1];
  try {
    const payload = jwt.verify(token, process.env.SECRET_KEY);
    const user = await User.findById(payload._id);
    if (!user) {
      return res.sendStatus(401);
    }
    res.send('You have accessed a secured route!');
  } catch (err) {
    return res.sendStatus(401);
  }
});

// Start server
app.listen(3000, () => console.log('Server started on port 3000'));