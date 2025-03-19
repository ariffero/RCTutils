// Do NOT change. Changes will be lost next time file is generated

#define R__DICTIONARY_FILENAME dict_ccdb
#define R__NO_DEPRECATION

/*******************************************************************/
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#define G__DICTIONARY
#include "ROOT/RConfig.hxx"
#include "TClass.h"
#include "TDictAttributeMap.h"
#include "TInterpreter.h"
#include "TROOT.h"
#include "TBuffer.h"
#include "TMemberInspector.h"
#include "TInterpreter.h"
#include "TVirtualMutex.h"
#include "TError.h"

#ifndef G__ROOT
#define G__ROOT
#endif

#include "RtypesImp.h"
#include "TIsAProxy.h"
#include "TFileMergeInfo.h"
#include <algorithm>
#include "TCollectionProxyInfo.h"
/*******************************************************************/

#include "TDataMember.h"

// Header files passed as explicit arguments
#include "dict_ccdb.h"

// Header files passed via #pragma extra_include

// The generated code does not explicitly qualify STL entities
namespace std {} using namespace std;

namespace ROOT {
   static TClass *pairlEunsignedsPlongcOunsignedsPintgR_Dictionary();
   static void pairlEunsignedsPlongcOunsignedsPintgR_TClassManip(TClass*);
   static void *new_pairlEunsignedsPlongcOunsignedsPintgR(void *p = nullptr);
   static void *newArray_pairlEunsignedsPlongcOunsignedsPintgR(Long_t size, void *p);
   static void delete_pairlEunsignedsPlongcOunsignedsPintgR(void *p);
   static void deleteArray_pairlEunsignedsPlongcOunsignedsPintgR(void *p);
   static void destruct_pairlEunsignedsPlongcOunsignedsPintgR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const pair<unsigned long,unsigned int>*)
   {
      pair<unsigned long,unsigned int> *ptr = nullptr;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(pair<unsigned long,unsigned int>));
      static ::ROOT::TGenericClassInfo 
         instance("pair<unsigned long,unsigned int>", "string", 187,
                  typeid(pair<unsigned long,unsigned int>), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &pairlEunsignedsPlongcOunsignedsPintgR_Dictionary, isa_proxy, 4,
                  sizeof(pair<unsigned long,unsigned int>) );
      instance.SetNew(&new_pairlEunsignedsPlongcOunsignedsPintgR);
      instance.SetNewArray(&newArray_pairlEunsignedsPlongcOunsignedsPintgR);
      instance.SetDelete(&delete_pairlEunsignedsPlongcOunsignedsPintgR);
      instance.SetDeleteArray(&deleteArray_pairlEunsignedsPlongcOunsignedsPintgR);
      instance.SetDestructor(&destruct_pairlEunsignedsPlongcOunsignedsPintgR);

      instance.AdoptAlternate(::ROOT::AddClassAlternate("pair<unsigned long,unsigned int>","pair<uint64_t,uint32_t>"));

      instance.AdoptAlternate(::ROOT::AddClassAlternate("pair<unsigned long,unsigned int>","std::pair<unsigned long, unsigned int>"));
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal(static_cast<const pair<unsigned long,unsigned int>*>(nullptr)); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *pairlEunsignedsPlongcOunsignedsPintgR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal(static_cast<const pair<unsigned long,unsigned int>*>(nullptr))->GetClass();
      pairlEunsignedsPlongcOunsignedsPintgR_TClassManip(theClass);
   return theClass;
   }

   static void pairlEunsignedsPlongcOunsignedsPintgR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_pairlEunsignedsPlongcOunsignedsPintgR(void *p) {
      return  p ? ::new(static_cast<::ROOT::Internal::TOperatorNewHelper*>(p)) pair<unsigned long,unsigned int> : new pair<unsigned long,unsigned int>;
   }
   static void *newArray_pairlEunsignedsPlongcOunsignedsPintgR(Long_t nElements, void *p) {
      return p ? ::new(static_cast<::ROOT::Internal::TOperatorNewHelper*>(p)) pair<unsigned long,unsigned int>[nElements] : new pair<unsigned long,unsigned int>[nElements];
   }
   // Wrapper around operator delete
   static void delete_pairlEunsignedsPlongcOunsignedsPintgR(void *p) {
      delete (static_cast<pair<unsigned long,unsigned int>*>(p));
   }
   static void deleteArray_pairlEunsignedsPlongcOunsignedsPintgR(void *p) {
      delete [] (static_cast<pair<unsigned long,unsigned int>*>(p));
   }
   static void destruct_pairlEunsignedsPlongcOunsignedsPintgR(void *p) {
      typedef pair<unsigned long,unsigned int> current_t;
      (static_cast<current_t*>(p))->~current_t();
   }
} // end of namespace ROOT for class pair<unsigned long,unsigned int>

namespace ROOT {
   static TClass *maplEunsignedsPlongcOunsignedsPintgR_Dictionary();
   static void maplEunsignedsPlongcOunsignedsPintgR_TClassManip(TClass*);
   static void *new_maplEunsignedsPlongcOunsignedsPintgR(void *p = nullptr);
   static void *newArray_maplEunsignedsPlongcOunsignedsPintgR(Long_t size, void *p);
   static void delete_maplEunsignedsPlongcOunsignedsPintgR(void *p);
   static void deleteArray_maplEunsignedsPlongcOunsignedsPintgR(void *p);
   static void destruct_maplEunsignedsPlongcOunsignedsPintgR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const map<unsigned long,unsigned int>*)
   {
      map<unsigned long,unsigned int> *ptr = nullptr;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(map<unsigned long,unsigned int>));
      static ::ROOT::TGenericClassInfo 
         instance("map<unsigned long,unsigned int>", -2, "map", 102,
                  typeid(map<unsigned long,unsigned int>), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &maplEunsignedsPlongcOunsignedsPintgR_Dictionary, isa_proxy, 4,
                  sizeof(map<unsigned long,unsigned int>) );
      instance.SetNew(&new_maplEunsignedsPlongcOunsignedsPintgR);
      instance.SetNewArray(&newArray_maplEunsignedsPlongcOunsignedsPintgR);
      instance.SetDelete(&delete_maplEunsignedsPlongcOunsignedsPintgR);
      instance.SetDeleteArray(&deleteArray_maplEunsignedsPlongcOunsignedsPintgR);
      instance.SetDestructor(&destruct_maplEunsignedsPlongcOunsignedsPintgR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::MapInsert< map<unsigned long,unsigned int> >()));

      instance.AdoptAlternate(::ROOT::AddClassAlternate("map<unsigned long,unsigned int>","std::map<unsigned long, unsigned int, std::less<unsigned long>, std::allocator<std::pair<unsigned long const, unsigned int> > >"));
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal(static_cast<const map<unsigned long,unsigned int>*>(nullptr)); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *maplEunsignedsPlongcOunsignedsPintgR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal(static_cast<const map<unsigned long,unsigned int>*>(nullptr))->GetClass();
      maplEunsignedsPlongcOunsignedsPintgR_TClassManip(theClass);
   return theClass;
   }

   static void maplEunsignedsPlongcOunsignedsPintgR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_maplEunsignedsPlongcOunsignedsPintgR(void *p) {
      return  p ? ::new(static_cast<::ROOT::Internal::TOperatorNewHelper*>(p)) map<unsigned long,unsigned int> : new map<unsigned long,unsigned int>;
   }
   static void *newArray_maplEunsignedsPlongcOunsignedsPintgR(Long_t nElements, void *p) {
      return p ? ::new(static_cast<::ROOT::Internal::TOperatorNewHelper*>(p)) map<unsigned long,unsigned int>[nElements] : new map<unsigned long,unsigned int>[nElements];
   }
   // Wrapper around operator delete
   static void delete_maplEunsignedsPlongcOunsignedsPintgR(void *p) {
      delete (static_cast<map<unsigned long,unsigned int>*>(p));
   }
   static void deleteArray_maplEunsignedsPlongcOunsignedsPintgR(void *p) {
      delete [] (static_cast<map<unsigned long,unsigned int>*>(p));
   }
   static void destruct_maplEunsignedsPlongcOunsignedsPintgR(void *p) {
      typedef map<unsigned long,unsigned int> current_t;
      (static_cast<current_t*>(p))->~current_t();
   }
} // end of namespace ROOT for class map<unsigned long,unsigned int>

namespace {
  void TriggerDictionaryInitialization_dict_ccdb_Impl() {
    static const char* headers[] = {
"dict_ccdb.h",
nullptr
    };
    static const char* includePaths[] = {
"/cvmfs/alice.cern.ch/el9-x86_64/Packages/ROOT/v6-32-06-alice1-14/include/",
"/home/jian/dpg/RCTutils_or/CCDB/",
nullptr
    };
    static const char* fwdDeclCode = R"DICTFWDDCLS(
#line 1 "dict_ccdb dictionary forward declarations' payload"
#pragma clang diagnostic ignored "-Wkeyword-compat"
#pragma clang diagnostic ignored "-Wignored-attributes"
#pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
extern int __Cling_AutoLoading_Map;
namespace std{template <typename _T1, typename _T2> struct __attribute__((annotate("$clingAutoload$bits/stl_pair.h")))  __attribute__((annotate("$clingAutoload$string")))  pair;
}
namespace std{template <typename _Tp = void> struct __attribute__((annotate("$clingAutoload$bits/stl_function.h")))  __attribute__((annotate("$clingAutoload$string")))  less;
}
namespace std{template <typename _Tp> class __attribute__((annotate("$clingAutoload$bits/allocator.h")))  __attribute__((annotate("$clingAutoload$string")))  allocator;
}
)DICTFWDDCLS";
    static const char* payloadCode = R"DICTPAYLOAD(
#line 1 "dict_ccdb dictionary payload"


#define _BACKWARD_BACKWARD_WARNING_H
// Inline headers
#include "dict_ccdb.h"

#undef  _BACKWARD_BACKWARD_WARNING_H
)DICTPAYLOAD";
    static const char* classesHeaders[] = {
nullptr
};
    static bool isInitialized = false;
    if (!isInitialized) {
      TROOT::RegisterModule("dict_ccdb",
        headers, includePaths, payloadCode, fwdDeclCode,
        TriggerDictionaryInitialization_dict_ccdb_Impl, {}, classesHeaders, /*hasCxxModule*/false);
      isInitialized = true;
    }
  }
  static struct DictInit {
    DictInit() {
      TriggerDictionaryInitialization_dict_ccdb_Impl();
    }
  } __TheDictionaryInitializer;
}
void TriggerDictionaryInitialization_dict_ccdb() {
  TriggerDictionaryInitialization_dict_ccdb_Impl();
}
