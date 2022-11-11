using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Microsoft.MixedReality.Toolkit;
public class InputManager : MonoBehaviour
{

    public Vector3 gazePosition;
    public Vector3 gazeNormalPosition;
    public ControllerLookup controllerLookup;
    int positionInLine;
    bool isValidTarget;
    // Start is called before the first frame update

    GLTFast.GltfAsset gltf;
    void generateCustomFromURL(string url, float scale)
    {
        Debug.Log("Generate planets GLTF");
        ImportGLTF(url, 0.3f);
    }

    void ImportGLTF(string filepath, float scale)
    {
        var empty = new GameObject();
        gltf = empty.AddComponent<GLTFast.GltfAsset>();
        gltf.url = Application.dataPath + "/Resources/doughnut.glb";

        Vector3 forwardPosition = Camera.main.transform.rotation * Vector3.forward * 0.5f;
        Vector3 finalPosition = Camera.main.transform.position + forwardPosition;
        gltf.transform.localPosition = finalPosition;
        //gltf.transform.localScale = new Vector3(1f, 1f, 1f);
        empty.transform.localScale = new Vector3(scale, scale, scale);
        // empty.AddComponent<BoxCollider>();
        // empty.AddComponent<BoundsControl>();
        // empty.AddComponent<ObjectManipulator>();
        // empty.AddComponent<ConstraintManager>();

        Debug.Log("Generatated");
    }

    void Start()
    {

        var empty = new GameObject();
        gltf = empty.AddComponent<GLTFast.GltfAsset>();
        gltf.url = Application.dataPath + "/Resources/doughnut.glb";

        Vector3 forwardPosition = Camera.main.transform.rotation * Vector3.forward * 0.5f;
        Vector3 finalPosition = Camera.main.transform.position + forwardPosition;
        gltf.transform.localPosition = finalPosition;
        //gltf.transform.localScale = new Vector3(1f, 1f, 1f);
        empty.transform.localScale = new Vector3(0.3f, 0.3f, 0.3f);

    }

    // Update is called once per frame
    void Update()
    {
        Debug.Log(controllerLookup);
        gltf.transform.localPosition = controllerLookup.GazeController.transform.position + 1f * controllerLookup.GazeController.transform.forward;
        Debug.Log(controllerLookup.GazeController.transform.position);
    }
}
