/*
 * Copyright (c) 2014      Intel, Inc. All rights reserved.
 * $COPYRIGHT$
 *
 * Additional copyrights may follow
 *
 * $HEADER$
 */

#ifndef MCA_PVSN_H
#define MCA_PVSN_H

/*
 * includes
 */

#include "orcm_config.h"
#include "orcm/constants.h"

#include "opal/mca/mca.h"
#include "opal/mca/event/event.h"
#include "opal/util/output.h"

#include "orte/runtime/orte_globals.h"
#include "orte/util/name_fns.h"
#include "orte/util/proc_info.h"

BEGIN_C_DECLS

/*
 * Component functions - all MUST be provided!
 */

/* initialize the selected module */
typedef int (*orcm_pvsn_base_module_init_fn_t)(void);

/* finalize the selected module */
typedef void (*orcm_pvsn_base_module_finalize_fn_t)(void);

/* calibrate */
typedef void (*orcm_pvsn_base_module_provision_fn_t)(void);

/*
 * Ver 1.0
 */
typedef struct {
    orcm_pvsn_base_module_init_fn_t        init;
    orcm_pvsn_base_module_finalize_fn_t    finalize;
    orcm_pvsn_base_module_provision_fn_t   provision;
} orcm_pvsn_base_module_t;

/*
 * the standard component data structure
 */
typedef struct {
    mca_base_component_t base_version;
    mca_base_component_data_t base_data;
} orcm_pvsn_base_component_t;

/*
 * Macro for use in components that are of type pvsn v1.0.0
 */
#define ORCM_PVSN_BASE_VERSION_1_0_0 \
  /* pvsn v1.0 is chained to MCA v2.0 */ \
  MCA_BASE_VERSION_2_0_0, \
  /* pvsn v1.0 */ \
  "pvsn", 1, 0, 0

/* Global structure for accessing name server functions
 */
ORCM_DECLSPEC extern orcm_pvsn_base_module_t orcm_pvsn;  /* holds API function pointers */

END_C_DECLS

#endif
