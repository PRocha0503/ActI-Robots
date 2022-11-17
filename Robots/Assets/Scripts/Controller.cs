/*
Pablo Rocha
Agents Controller
*/

using System;
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;
public class RobotData
{
    public int uniqueID;
    public Vector3 position;
}

public class BoxData
{
    public List<Vector3> positions;
}
public class DBInit{
    public int numberOfBoxes;
    public int width;
    public int height;
    public int maxFrames;
}
public class Request  
{  
    public string error;
    public UnityEngine.Networking.UnityWebRequest.Result result;
    public string response; 
    public long responseCode;
}  

public class Controller : MonoBehaviour
{
     string serverUrl = "http://localhost:8585";
    string sendConfigEndpoint = "/init";
    string getRobotsEndpoint = "/robots";
    string getBoxesEndpoint = "/boxes";
    string updateEndpoint = "/step";
    BoxData robotsData, boxData;
    GameObject[] robots;
    GameObject[] boxes;
    GameObject[] walls;
    List<Vector3> oldPositions;
    List<Vector3> newPositions;
    List<Vector3> oldBoxPositions;
    List<Vector3> newBoxPositions;
    // Pause the simulation while we get the update from the server
    bool hold = false;

    public GameObject robotPrefab, boxPrefab, floor,wallPrefab,camara;
    public int numberOfBoxes, width, height;
    public float timeToUpdate = 5.0f, timer, dt;
    // Start is called before the first frame update
    void Start()
    {
        //Inizialize variables
        robotsData = new BoxData();
        boxData = new BoxData();
        oldPositions = new List<Vector3>();
        newPositions = new List<Vector3>();
        oldBoxPositions = new List<Vector3>();
        newBoxPositions = new List<Vector3>();

        robots = new GameObject[5];
        boxes = new GameObject[numberOfBoxes];
        walls = new GameObject[4];
        

        floor.transform.localScale = new Vector3((float)width/10, 1, (float)height/10);
        floor.transform.localPosition = new Vector3((float)width/2-0.5f, 0, (float)height/2-0.5f);
        
        timer = timeToUpdate;

        for(int i = 0; i < 5; i++)
            robots[i] = Instantiate(robotPrefab, Vector3.zero, Quaternion.identity);
        for(int i = 0; i < numberOfBoxes; i++)
            boxes[i] = Instantiate(boxPrefab, Vector3.zero, Quaternion.identity);
        //Walls
        walls[0] = Instantiate(wallPrefab, new Vector3(-0.5f, 0, (float)height/2-0.5f), Quaternion.identity);
        walls[0].transform.localScale = new Vector3(0.1f, 1, (float)height);
        walls[1] = Instantiate(wallPrefab, new Vector3((float)width-0.5f, 0, (float)height/2-0.5f), Quaternion.identity);
        walls[1].transform.localScale = new Vector3(0.1f, 1, (float)height);
        walls[2] = Instantiate(wallPrefab, new Vector3((float)width/2-0.5f, 0, -0.5f), Quaternion.identity);
        walls[2].transform.localScale = new Vector3((float)width, 1, 0.1f);     
        walls[3] = Instantiate(wallPrefab, new Vector3((float)width/2-0.5f, 0, (float)height-0.5f), Quaternion.identity);
        walls[3].transform.localScale = new Vector3((float)width, 1, 0.1f);
        //Move camara to corner
        camara.transform.position = new Vector3(0, 10, 0);
        camara.transform.LookAt(new Vector3((float)width/2, 0, (float)height/2));


            
            
        StartCoroutine(SendConfiguration());

    }

    // Update is called once per frame
    private void Update() 
    {
        float t = timer/timeToUpdate;
        // Smooth out the transition at start and end
        dt = t * t * ( 3f - 2f*t);

        if(timer >= timeToUpdate)
        {
            timer = 0;
            hold = true;
            StartCoroutine(UpdateSimulation());
        }

        if (!hold)
        {
            for (int s = 0; s < robots.Length; s++)
            {
                Vector3 interpolated = Vector3.Lerp(oldPositions[s], newPositions[s], dt);
                robots[s].transform.localPosition = interpolated;
                
                Vector3 dir = oldPositions[s] - newPositions[s];
                robots[s].transform.rotation = Quaternion.LookRotation(dir);
                
            }
            for (int s = 0; s < boxes.Length; s++)
            {
                Vector3 interpolated = Vector3.Lerp(oldBoxPositions[s], newBoxPositions[s], dt);
                boxes[s].transform.localPosition = interpolated;
                Vector3 dir = oldBoxPositions[s] - newBoxPositions[s];
                boxes[s].transform.rotation = Quaternion.LookRotation(dir);
                
            }

            // Move time from the last frame
            timer += Time.deltaTime;
        }
    }
    IEnumerator SendConfiguration()
    {
        DBInit dbInit = new DBInit();
        dbInit.numberOfBoxes = numberOfBoxes;
        dbInit.width = width;
        dbInit.height = height;
        dbInit.maxFrames = 1000;
        string json = JsonUtility.ToJson(dbInit);
        using (UnityWebRequest www = UnityWebRequest.Put(serverUrl + sendConfigEndpoint,json))
        {
        www.method = "POST";
        www.SetRequestHeader("Content-Type", "application/json");
        // Request and wait for the desired page.
        yield return www.SendWebRequest();
        Request req = new Request();
        req.result = www.result;
        req.error = www.error;
        req.response =  www.downloadHandler.text;
        req.responseCode= www.responseCode;
        if (req.result == UnityWebRequest.Result.Success)
        {
            Debug.Log("Configuration sent");
            StartCoroutine(GetRobots());
            StartCoroutine(GetBoxes());
        }
        else
        {
            Debug.Log("Error sending configuration");
        }
        }
    }
    public IEnumerator GetRobots()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getRobotsEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            robotsData = JsonUtility.FromJson<BoxData>(www.downloadHandler.text);

            // Store the old positions for each agent
            oldPositions = new List<Vector3>(newPositions);

            newPositions.Clear();

            foreach(Vector3 v in robotsData.positions)
                newPositions.Add(v);
        }
    }
    public IEnumerator GetBoxes()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getBoxesEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            boxData = JsonUtility.FromJson<BoxData>(www.downloadHandler.text);

            oldBoxPositions = new List<Vector3>(newBoxPositions);

            newBoxPositions.Clear();

            foreach(Vector3 v in boxData.positions)
                newBoxPositions.Add(v);

            hold = false;
        }
    }
    IEnumerator UpdateSimulation()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + updateEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            StartCoroutine(GetRobots());
            StartCoroutine(GetBoxes());
        }
    }


}
