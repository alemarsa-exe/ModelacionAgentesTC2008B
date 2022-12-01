// TC2008B. Sistemas Multiagentes y Gráficas Computacionales
// C# client to interact with Python. Based on the code provided by Sergio Ruiz.
// Octavio Navarro. November 2022

using System;
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;

[Serializable]
public class BoidData
{
    public string carId, lightId;
    public float x, y, z;
    public int typeCar;

    public BoidData(string carId, float x, float y, float z, int typeCar)
    {
        this.carId = carId;
        this.x = x;
        this.y = y;
        this.z = z;
        this.typeCar = typeCar;
    }
}

[Serializable]
public class BoidsData
{
    public List<BoidData> positions;

    public BoidsData() => this.positions = new List<BoidData>();
}

[Serializable]
public class TrafficData
{
    public string lightId;
    public string state;

    public TrafficData(string lightId, string state)
    {
        this.lightId = lightId;
        this.state = state;
    }
}

[Serializable]
public class TrafficsData
{
    public List<TrafficData> trafficStates;
    public TrafficsData() => this.trafficStates = new List<TrafficData>();
}

public class AgentControllerUpdate : MonoBehaviour
{
    private string uri = "http://localhost:8585";
    // private string uri = "http://multiagentesintegradora.us-south.cf.appdomain.cloud/";

    BoidsData boidsData;
    TrafficsData trafficsData;

    Dictionary<string, Vector3> boidsPrevPositions, boidsCurrPositions;
    public GameObject[] agentPrefab;
    Dictionary<string, GameObject> agents;
    public float timeToUpdate = 20.0f;
    private float timer, dt;
    private bool started = false, updated = false;

    void Start()
    {
        boidsData = new BoidsData();
        trafficsData = new TrafficsData();

        agents = new Dictionary<string, GameObject>();

        boidsPrevPositions = new Dictionary<string, Vector3>();
        boidsCurrPositions = new Dictionary<string, Vector3>();

        timer = timeToUpdate;

        StartCoroutine(StartSimulation());        
    }
 
    IEnumerator StartSimulation()
    {
        using(UnityWebRequest webRequest = UnityWebRequest.Get($"{uri}/init"))
        {
            Debug.Log("Starting...");
            yield return webRequest.SendWebRequest();

            if (webRequest.result != UnityWebRequest.Result.Success)
            {
                Debug.Log(webRequest.error);
            }
            else
            {
                Debug.Log($" Starting simulation with: {webRequest.downloadHandler.text}");
                
                StartCoroutine(GetBoidsData());
                StartCoroutine(GetTrafficData());
            }
        }    
    }

    IEnumerator GetBoidsData() 
    {
        using(UnityWebRequest webRequest = UnityWebRequest.Get($"{uri}/init"))
        {
            yield return webRequest.SendWebRequest();

            if (webRequest.result != UnityWebRequest.Result.Success)
                Debug.Log(webRequest.error);
            else 
            {
                Debug.Log(webRequest.downloadHandler.text);
                boidsData = JsonUtility.FromJson<BoidsData>(webRequest.downloadHandler.text);

                foreach(BoidData boid in boidsData.positions)
                {
                    Vector3 newBoidPosition = new Vector3(boid.x, boid.y, boid.z);
                    GameObject newAgent;
                    
                    if (boid.typeCar == 1)
                    {
                        newAgent = agentPrefab[0];
                        //newAgent = GameObject.Find("Ferrari");
                    }
                    // ESTOS SON BUENOS
                    else if (boid.typeCar == 2)
                    {
                        newAgent = agentPrefab[1];
                        //newAgent = GameObject.Find("Camion");
                    }
                    else if (boid.typeCar == 3)
                    {
                        newAgent = agentPrefab[2];
                        //newAgent = GameObject.Find("RB18");
                    }
                    else 
                    {
                        newAgent = agentPrefab[3];
                        //newAgent = GameObject.Find("Helados");
                    }


                    /// Otra cosa



                    // else if (boid.typeCar == "<class 'agent.CarAgentDifferentB'>")
                    // {
                    //     newAgent = agentPrefab[2];
                    // }
                    // else if (boid.typeCar == "<class 'agent.CarAgentDifferentC'>")
                    // {
                    //     newAgent = agentPrefab[3];
                    
                    

                    if(!started)
                    {
                        boidsPrevPositions[boid.carId] = newBoidPosition;
                        agents[boid.carId] = Instantiate(newAgent, newBoidPosition, Quaternion.identity);
                    }
                    else
                    {
                        Vector3 currentPosition = new Vector3();
                        if(boidsCurrPositions.TryGetValue(boid.carId, out currentPosition))
                            boidsPrevPositions[boid.carId] = currentPosition;
                        boidsCurrPositions[boid.carId] = newBoidPosition;
                    }
                }

                updated = true;
                if(!started) started = true;
            }
        }        
    }

    IEnumerator GetTrafficData()
    {
        using(UnityWebRequest webRequest = UnityWebRequest.Get($"{uri}/init"))
        {
            yield return webRequest.SendWebRequest();

            if (webRequest.result != UnityWebRequest.Result.Success)
                Debug.Log(webRequest.error);
            else 
            {
                Debug.Log(webRequest.downloadHandler.text);
                trafficsData = JsonUtility.FromJson<TrafficsData>(webRequest.downloadHandler.text);
                foreach(TrafficData traffic in trafficsData.trafficStates)
                {
                    Debug.Log(traffic.lightId);
                    
                    if(traffic.lightId == "36" | traffic.lightId  == "37")
                    {
                        Light light = GameObject.Find("1newSemaforo1").GetComponent<Light>();
                        if(traffic.state == "Green")
                        {
                            light.color = Color.green;
                        }
                        if(traffic.state == "Yellow")
                        {
                            light.color = Color.yellow;
                        }
                        if(traffic.state == "Red")
                        {
                            light.color = Color.red;
                        }

                    }
                    if(traffic.lightId == "38" | traffic.lightId  == "39")
                    {
                        Light light = GameObject.Find("2newSemaforo2").GetComponent<Light>();
                        if(traffic.state == "Green")
                        {
                            light.color = Color.green;
                        }
                        if(traffic.state == "Yellow")
                        {
                            light.color = Color.yellow;
                        }
                        if(traffic.state == "Red")
                        {
                            light.color = Color.red;
                        }

                    }
                    if(traffic.lightId == "40" | traffic.lightId  == "41")
                    {
                        Light light = GameObject.Find("3newSemaforo3").GetComponent<Light>();
                        if(traffic.state == "Green")
                        {
                            light.color = Color.green;
                        }
                        if(traffic.state == "Yellow")
                        {
                            light.color = Color.yellow;
                        }
                        if(traffic.state == "Red")
                        {
                            light.color = Color.red;
                        }

                    }
                    if(traffic.lightId == "42" | traffic.lightId  == "43")
                    {
                        UnityEngine.Light light = GameObject.Find("4newSemaforo4").GetComponent<Light>();
                        if(traffic.state == "Green")
                        {
                            light.color = new Color(0.0f, 255.0f, 0.0f);
                        }
                        if(traffic.state == "Yellow") // comment
                        {
                            light.color = Color.yellow;
                        }
                        if(traffic.state == "Red")
                        {
                            light.GetComponent<Light>().color = new Color(255.0f, 0.0f, 0.0f); 
                        }

                    }
                }

                updated = true;
            }
        }
    }

    void Update()
    {
        if(updated)
        {
            timer -= Time.deltaTime;
            dt = 1.0f - (timer / timeToUpdate);
        }

        if(timer < 0)
        {
            timer = timeToUpdate; 
            updated = false;
            StartCoroutine(GetBoidsData());  
        }

        foreach(var boid in boidsCurrPositions)
        {
            Vector3 currentPosition = boid.Value;
            Vector3 previousPosition = boidsPrevPositions[boid.Key];

            Vector3 interpolated = Vector3.Lerp(previousPosition, currentPosition, dt);
            Vector3 direction = currentPosition - previousPosition;

            agents[boid.Key].transform.localPosition = interpolated;
            agents[boid.Key].transform.rotation = Quaternion.LookRotation(direction);
        }
    }
}
