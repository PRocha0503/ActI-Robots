using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BoxController : MonoBehaviour
{
    [SerializeField] MeshRenderer meshRenderer;
    private bool carried;
    private bool dropped;

    private void Start()
    {
        Invisible(false);
    }

    public void Invisible(bool invisible)
    {
        if (!invisible)
            dropped = true;
        
        meshRenderer.enabled = !invisible;
    }
    
    
    public bool GetIsCarried()
    {
        return carried;
    }

    public bool GetIsDropped()
    {
        return dropped;
    }
}
