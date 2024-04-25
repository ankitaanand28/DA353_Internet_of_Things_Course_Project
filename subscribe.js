const mqtt = require('mqtt');
const { MongoClient } = require('mongodb');

// MQTT connection parameters
const mqttOptions = {
    host: 'f2a2c50d3bf143cb86d175f6306f9781.s1.eu.hivemq.cloud',
    port: 8883,
    protocol: 'mqtts',
    username: 'Shivam',
    password: 'Shivam@123'
};

// MongoDB URI
const mongoURI = "mongodb+srv://Shivam:Shivam@agriculture.y46nprf.mongodb.net/?retryWrites=true&w=majority&appName=Agriculture";

// Initialize MQTT client
const mqttClient = mqtt.connect(mqttOptions);

// Initialize MongoDB client
const mongoClient = new MongoClient(mongoURI, { useNewUrlParser: true, useUnifiedTopology: true });

// MQTT connection callback
mqttClient.on('connect', function () {
    console.log('Connected to MQTT');
    // Subscribe to topic 'SensorData' upon successful connection
    mqttClient.subscribe('SensorData', function (err) {
        if (!err) {
            console.log('Subscribed to SensorData topic');
        }
    });
});

// MQTT error callback
mqttClient.on('error', function (error) {
    console.error('MQTT Error:', error);
});

// MongoDB connection function
async function connectToMongoDB() {
    try {
        // Connect to MongoDB
        await mongoClient.connect();
        console.log('Connected to MongoDB');
    } catch (error) {
        console.error('MongoDB Connection Error:', error);
    }
}

// MongoDB insertion function
async function insertDocumentToMongoDB(document) {
    try {
        // Access the 'agridata' database
        const database = mongoClient.db('agridata');
        // Access the 'parameter' collection
        const collection = database.collection('parameter');
        // Insert the document into the collection
        await collection.insertOne(document);
        console.log("Document inserted into MongoDB successfully.");
    } catch (error) {
        console.error('MongoDB Insertion Error:', error);
    }
}

mqttClient.on('message', function (topic, message) {
    console.log('Received message:', topic, message.toString());
    try {
        // Remove the curly braces and split the string into key-value pairs
        const keyValuePairs = message.toString().replace(/[{}]/g, '').split(', ');
        // Initialize an empty object to store parsed data
        const data = {};
        // Iterate over the key-value pairs and parse them
        keyValuePairs.forEach(pair => {
            // Split each pair into key and value
            const [key, value] = pair.split(':');
            // Trim any whitespace and single quotes from keys and values
            const cleanKey = key.trim().replace(/'/g, '');
            const cleanValue = parseFloat(value.trim());
            // Add the parsed key-value pair to the data object
            data[cleanKey] = cleanValue;
        });
        // Insert the parsed message into MongoDB
        insertDocumentToMongoDB(data);
    } catch (error) {
        console.error('Message Parsing Error:', error);
    }
});

// Call the function to connect to MongoDB
connectToMongoDB().catch(console.error);
