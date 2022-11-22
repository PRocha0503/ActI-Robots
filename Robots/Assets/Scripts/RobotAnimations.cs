using System;
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;

public class RobotAnimations : MonoBehaviour
{
    [SerializeField] private Animator animator;
    [SerializeField] private float boxCheckRange = 0.5f;
    private GameObject box;
    private Vector3[] raycastDirections;
    bool carryingBox = false;
    private RaycastHit hit;
    private Quaternion startingRotation;

    // Start is called before the first frame update
    void Start()
    {
        startingRotation = transform.rotation;
        raycastDirections = new[] { Vector3.forward, Vector3.back, Vector3.left, Vector3.right };
    }

    // Update is called once per frame
    void Update()
    {
        foreach (var raycastDirection in raycastDirections)
        {
            if (Physics.Raycast(transform.position, raycastDirection, out hit, boxCheckRange))
            {
                if (hit.collider.gameObject.CompareTag("Box") && !hit.transform.GetComponent<BoxController>().GetIsCarried() && !hit.transform.GetComponent<BoxController>().GetIsDropped())
                {
                    PickUpBox();
                }
            }
        }
    }

    private void PickUpBox()
    {
        if (carryingBox) return;
        box = hit.collider.gameObject;
        box.GetComponent<BoxController>().Invisible(true);
        animator.SetTrigger("BoxUp");
        carryingBox = true;
    }

    private void DropBox()
    {
        Debug.Log("Dropping Box");
        animator.SetTrigger("BoxDown");
        box.GetComponent<BoxController>().Invisible(false);
        carryingBox = false;
    }

    private void OnTriggerExit(Collider other)
    {
        if (other.gameObject.CompareTag("Box") && carryingBox)
        {
            //other.GetComponent<BoxController>().Invisible(false);
            DropBox();
        }
    }

    private void OnDrawGizmos()
    {
        foreach (var raycastDirection in raycastDirections)
        {
            Gizmos.color = Color.red;
            Gizmos.DrawRay(transform.position, raycastDirection * boxCheckRange);
        }
    }
}
